from typing import Optional
from datetime import datetime
from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command
import os
import json

class ModSet(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name = "modset", aliases = ["mset","modsettings"], attr = [])
    async def modset (self, ctx, target: Optional[Member]):
        pass
    @command(name = "changepref", aliases = ["changeprefix"])
    async def change_prefix(self, ctx, prefix: Optional[str]):
        if ctx.guild.id == int(os.environ['PUBLIC_BOT_SERVER']):
            embed = Embed(title = "Status",
                     colour = 0xff0000,
                     timestamp = datetime.utcnow())
            embed.add_field(name="Error", value="Prefix changes are not allowed on this server!", inline=True)
            await ctx.send(embed=embed)
        else:
            if prefix:
                with open('./data/prefixes.json', 'r') as pref:
                    prefixes = json.load(pref)
                prefixes[str(ctx.guild.id)] = prefix
                embed = Embed(title = "Status",
                         colour = 0x00ff00,
                         timestamp = datetime.utcnow())
                embed.add_field(name="Done", value="New Prefix is " + prefix, inline=True)
                await ctx.send(embed=embed)
                with open('./data/prefixes.json', 'w') as pref:
                    json.dump(prefixes, pref, indent = 4)
            else:
                embed = Embed(title = "Status",
                         colour = 0xff0000,
                         timestamp = datetime.utcnow())
                embed.add_field(name="Error", value="Blank prefixes not allowed!", inline=True)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ModSet(bot))