import logging
from datetime import datetime

import discord
from discord import Status
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from config.settings import core_config


def get_time():
    now = datetime.now()
    currentTime = now.strftime("%m-%d-%Y-%H-%M-%S")
    return currentTime


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.first_start = True

    @commands.Cog.listener()
    async def on_ready(self):
        if self.first_start:
            if core_config['custom_status'] != '':
                await self.bot.change_presence(status=Status.online, activity=discord.Game(core_config['custom_status']))
            else:
                await self.bot.change_presence(status=Status.online)
            self.first_start = False
            logging.basicConfig(filename='./logs/bot' + get_time() + '.log',
                                filemode='a',
                                format='%(name)s - %(levelname)s - %(message)s',
                                level=logging.INFO)
            logging.info('------------------------------------------------')
            logging.info('Bot started at ' + get_time())
            logging.info('------------------------------------------------')
            print("Bot Ready")

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.info('Bot disconnected at ' + get_time())

    @commands.command()
    @has_permissions(administrator=True)
    async def stop(self, ctx):
        await ctx.send('Stopping')
        logging.info('------------------------------------------------')
        logging.info('Bot stopped at ' + get_time())
        logging.info('------------------------------------------------')
        await self.bot.change_presence(status=Status.offline)
        await self.bot.close()
        print('Stopping')

    @stop.error
    async def stop_error(self, ctx, error):
        if isinstance(error, CheckFailure):
            await ctx.send("no u")
