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

    @command(name = "modset", aliases = ["mset","modsettings"])
    async def modset (self, ctx, target: Optional[Member]):
        pass
    @command(name = "tags", aliases = ["tagging","msgtag"], help = "toggles message tags")
    async def message_tags(self, ctx, switch: Optional[str]):
        with open('./data/tag_messages.json', 'r') as tag_:
            tag_messages=json.load(tag_)
        if switch is None:
            if tag_messages[str(ctx.guild.id)] == "off":
                tag_messages[str(ctx.guild.id)] = "on"
            else:
                tag_messages[str(ctx.guild.id)] = "off"
        elif switch.lower() == "off" or switch == "0":
            tag_messages[str(ctx.guild.id)] = "off"
        elif switch.lower() == "on" or switch == "1":
            tag_messages[str(ctx.guild.id)] = "on"
        
        else:
            embed=Embed(title="Status",colour=0xff0000,timestamp = datetime.utcnow())
            embed.add_field(name="Error", value="Invalid value provided", inline=True)
            await ctx.send(embed=embed)
            return
        
        embed = Embed(title = "Status",
                 colour = 0x00ff00,
                 timestamp = datetime.utcnow())
        
        with open('./data/tag_messages.json', 'w') as tag_:
            json.dump(tag_messages, tag_, indent = 4)
        embed.add_field(name="Done", value="Message Tags are now " + tag_messages[str(ctx.guild.id)], inline=True)
        await ctx.send(embed=embed)

    @command(name = "changepref", aliases = ["changeprefix"], help="changes the prefix to the appended string")
    async def change_prefix(self, ctx, prefix: Optional[str]):
        if ctx.guild.id == int(os.environ['PUBLIC_BOT_SERVER']):
            embed = Embed(title = "Status",
                     colour = 0xff0000,
                     timestamp = datetime.utcnow())
            embed.add_field(name="Error", value="Prefix changes are not allowed on this server!", inline=True)
            await ctx.send(embed=embed)
        else:
            if ctx.author != ctx.guild.owner:
                embed = Embed(title = "Status",
                         colour = 0xff0000,
                         timestamp = datetime.utcnow())
                embed.add_field(name="Error", value="Only server owner can change the prefix!", inline=True)
                await ctx.send(embed=embed)
                return
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