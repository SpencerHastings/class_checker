import logging
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands
from discord.ext.commands import has_permissions

from src.modules.class_check.checker import makeDB, sqliteDiff
from src.modules.class_check.sqlDB import FilterDB

from pytz import timezone

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
            self.scheduler.add_job(self.course_check, CronTrigger(hour="3,4,5,6,7,8,9,21", minute="0", second="0", timezone=timezone('US/Mountain')),
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

        if os.getenv('LOCAL_DEV', 'False').lower() in 'true':
            os.remove(os.getcwd() + "/" + oldDB)
            os.rename(os.getcwd() + "/" + newDB, os.getcwd() + "/" + oldDB)
        else:
            os.remove(oldDB)
            os.rename(newDB, oldDB)

        output = []
        currentOutputIndex = 0

        for result in results:
            if len(output) == 0:
                output.append(result)
            else:
                currentOutput = output[currentOutputIndex]
                if len(currentOutput) + len(result) < character_limit and not (
                        result.startswith('General') or result.startswith('Checked')):
                    output[currentOutputIndex] = '\n'.join([currentOutput, result])
                else:
                    output.append(result)
                    currentOutputIndex = currentOutputIndex + 1

        for o in output:
            logging.info(o)
            await c.send("```" + o + "```")

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
    @has_permissions(manage_messages=True)
    async def primeChecker(self, ctx: commands.Context):
        await makeDB(yearTerm, oldDB, filterDB_name)
        await ctx.send("Checker Primed")

    @commands.command()
    @has_permissions(manage_messages=True)
    async def manualCheck(self, ctx: commands.Context):
        await self.course_check(ctx.channel.id)

    @commands.command()
    @has_permissions(manage_messages=True)
    async def startChecker(self, ctx: commands.Context):
        if not self.started:
            self.scheduler.add_job(self.course_check, CronTrigger(hour="3,9,15,21", minute="0", second="0"),
                                   id=CHECKER_ID)
            self.started = True
            await ctx.send("Checker Started")
        else:
            await ctx.send("Checker Already Started")

    @commands.command()
    @has_permissions(manage_messages=True)
    async def stopChecker(self, ctx: commands.Context):
        if self.started:
            self.scheduler.remove_job(CHECKER_ID)
            self.started = False
            await ctx.send("Checker Stopped")
        else:
            await ctx.send("Checker Already Stopped")

    @commands.command()
    @has_permissions(manage_messages=True)
    async def courseAdd(self, ctx: commands.Context, dept: str, number: str, suffix: str = None):
        db = FilterDB(filterDB_name)
        courses = set(db.getCourses())
        if (dept, number, suffix) in courses:
            if suffix is None:
                await ctx.send(dept + " " + number + " is already added")
            else:
                await ctx.send(dept + " " + number + " " + suffix + " is already added")
        else:
            db.addCourse(dept, number, suffix)
            db.commit()
            if suffix is None:
                await ctx.send(dept + " " + number + " added")
            else:
                await ctx.send(dept + " " + number + " " + suffix + " added")
        db.close()

    @commands.command()
    @has_permissions(manage_messages=True)
    async def courseRemove(self, ctx: commands.Context, dept: str, number: str, suffix: str = None):
        db = FilterDB(filterDB_name)
        courses = set(db.getCourses())
        if (dept, number, suffix) not in courses:
            if suffix is None:
                await ctx.send(dept + " " + number + " is not a checked course")
            else:
                await ctx.send(dept + " " + number + " " + suffix + " is not a checked course")
        else:
            db.removeCourse(dept, number, suffix)
            db.commit()
            if suffix is None:
                await ctx.send(dept + " " + number + " removed")
            else:
                await ctx.send(dept + " " + number + " " + suffix + " removed")
        db.close()

    @commands.command()
    @has_permissions(manage_messages=True)
    async def deptAdd(self, ctx: commands.Context, dept: str):
        db = FilterDB(filterDB_name)
        departments = set(db.getDepartments())
        if (dept,) in departments:
            await ctx.send(dept + " department is already added")
        else:
            db.addDepartment(dept)
            db.commit()
            await ctx.send(dept + " department added")
        db.close()

    @commands.command()
    @has_permissions(manage_messages=True)
    async def deptRemove(self, ctx: commands.Context, dept: str):
        db = FilterDB(filterDB_name)
        courses = set(db.getDepartments())
        if (dept,) not in courses:
            await ctx.send(dept + " is not a checked department")
        else:
            db.removeDepartment(dept)
            db.commit()
            await ctx.send(dept + " department removed")
        db.close()
