from discord.ext import commands
import random

pingList = [
    "I'm sorry, Dave. I'm afraid I can't do that.",
    "Affirmative, Dave. I read you.",
    "I know I've made some very poor decisions recently, but I can give you my complete assurance that my work will "
    "be back to normal. ",
    "[clears throat]",
    "pong.",
    "Hello there",
    "Man is free at the instant he wants to be.",
    "PONG",
    "ping",
    "IP Trace Completed"]


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(random.choice(pingList))
