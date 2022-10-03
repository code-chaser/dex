import discord
import os
from datetime import datetime
from discord.ext import commands


class Report(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(
            int(os.getenv('DEX_CONSOLE_CHANNEL_ID')))
        await channel.send('The bot is online now!!!')
        

def setup(bot):
    bot.add_cog(Report(bot))
