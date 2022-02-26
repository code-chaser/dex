from discord.ext.commands import Cog
from discord.ext.commands import command

class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name = "userinfo")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            