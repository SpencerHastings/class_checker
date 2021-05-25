import asyncio
import os

from discord.ext import commands

from cogs import add_cogs
from config.settings import prefix

token = os.getenv('DISCORD_TOKEN', '')

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

bot = commands.Bot(command_prefix=prefix)
add_cogs(bot)
bot.run(token)
