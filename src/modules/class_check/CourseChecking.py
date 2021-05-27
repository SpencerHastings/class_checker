import asyncio
import os
import logging

from apscheduler.triggers.date import DateTrigger
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from discord.ext.commands import has_permissions

from src.modules.class_check.checker import makeDB, sqliteDiff
from src.modules.class_check.sqlDB import FilterDB

CHECKER_ID = "checker_task"

yearTerm = '20215'
if os.getenv('LOCAL_DEV', 'False').lower() in 'true':
    oldDB = 'old.db'
    newDB = 'new.db'
    filterDB_name = "filters.db"
else:
    oldDB = '/data/old.db'
    newDB = '/data/new.db'
    filterDB_name = "/data/filters.db"
character_limit = 1800


class CourseChecking(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channelID = int(os.getenv('CHECK_CHANNEL_ID'))
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.started = False
        self.first_start = True

    @commands.Cog.listener()
    async def on_ready(self):
        if self.first_start:
            self.first_start = False
            self.scheduler.add_job(self.course_check, CronTrigger(hour="3,9,15,21", minute="0", second="0"),
                                   id=CHECKER_ID)
            self.started = True
            logging.info('Checker Started on Bot Run')

    async def course_check(self, channelID=None):
        await self.bot.wait_until_ready()
        if channelID is None:
            c = self.bot.get_channel(self.channelID)
        else:
            c = self.bot.get_channel(channelID)

        await makeDB(yearTerm, newDB, filterDB_name)

        results = sqliteDiff(oldDB, newDB)

        # if os.getenv('LOCAL_DEV', 'False').lower() in 'true':
        #     os.remove(os.getcwd() + "/" + oldDB)
        #     os.rename(os.getcwd() + "/" + newDB, os.getcwd() + "/" + oldDB)
        # else:
        #     os.remove(oldDB)
        #     os.rename(newDB, oldDB)

        output = ['']
        currentOutputIndex = 0

        for result in results:
            currentOutput = output[currentOutputIndex]
            if len(currentOutput) + len(result) < character_limit:
                output[currentOutputIndex] = '\n'.join([currentOutput, result])
            else:
                output.append(result)
                currentOutputIndex = currentOutputIndex + 1

        for o in output:
            logging.info(o)
            await c.send(o)

    @commands.command()
    async def checked(self, ctx: commands.Context):
        db = FilterDB(filterDB_name)
        results = []

        for course in db.getCourses():
            if course[2] is None:
                results.append(course[0] + " " + course[1])
            else:
                results.append(course[0] + " " + course[1] + " " + course[2])

        output = ['']
        currentOutputIndex = 0

        for result in results:
            currentOutput = output[currentOutputIndex]
            if len(currentOutput) + len(result) < character_limit:
                output[currentOutputIndex] = '\n'.join([currentOutput, result])
            else:
                output.append(result)
                currentOutputIndex = currentOutputIndex + 1

        for o in output:
            await ctx.send(o)

    @commands.command()
    @has_permissions(administrator=True)
    async def primeChecker(self, ctx: commands.Context):
        await makeDB(yearTerm, oldDB, filterDB_name)
        await ctx.send("Checker Primed")

    @commands.command()
    @has_permissions(administrator=True)
    async def manualCheck(self, ctx: commands.Context):
        await self.course_check(ctx.channel.id)

    @commands.command()
    @has_permissions(administrator=True)
    async def startChecker(self, ctx: commands.Context):
        if not self.started:
            self.scheduler.add_job(self.course_check, CronTrigger(hour="3,9,15,21", minute="0", second="0"),
                                   id=CHECKER_ID)
            self.started = True
            await ctx.send("Checker Started")
        else:
            await ctx.send("Checker Already Started")

    @commands.command()
    @has_permissions(administrator=True)
    async def stopChecker(self, ctx: commands.Context):
        if self.started:
            self.scheduler.remove_job(CHECKER_ID)
            self.started = False
            await ctx.send("Checker Stopped")
        else:
            await ctx.send("Checker Already Stopped")
