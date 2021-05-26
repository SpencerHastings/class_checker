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
oldDB = 'old.db'
newDB = 'new.db'


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

        await makeDB(yearTerm, newDB)

        results = sqliteDiff('old.db', 'new.db')

        os.remove(os.getcwd() + "/" + oldDB)
        os.rename(os.getcwd() + "/" + newDB, os.getcwd() + "/" + oldDB)

        output = ""

        for result in results:
            output = '\n'.join([output, result])

        logging.info(output)

        await c.send(output)

    @commands.command()
    async def checked(self, ctx: commands.Context):
        db = FilterDB('filters.db')
        results = []

        for course in db.getCourses():
            results.append(course[0])

        output = ""

        for result in results:
            output = '\n'.join([output, result])

        await ctx.send(output)

    @commands.command()
    @has_permissions(administrator=True)
    async def primeChecker(self, ctx: commands.Context):
        await makeDB(yearTerm, oldDB)
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
