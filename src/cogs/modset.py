import discord
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

    @command(name="modset", aliases=["mset", "modsettings"])
    async def modset(self, ctx, target: Optional[Member]):
        pass

    @command(name="tags", aliases=["tagging", "msgtag"], help="toggles message tags")
    async def message_tags(self, ctx, switch: Optional[str]):
        with open('./data/tag_messages.json', 'r') as tag_:
            tag_messages = json.load(tag_)
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
            embed = Embed(title="Status", colour=0xff0000,
                          timestamp=datetime.utcnow())
            embed.add_field(
                name="Error", value="Invalid value provided", inline=True)
            await ctx.send(embed=embed)
            return

        embed = Embed(title="Status",
                      colour=0x00ff00,
                      timestamp=datetime.utcnow())

        with open('./data/tag_messages.json', 'w') as tag_:
            json.dump(tag_messages, tag_, indent=4)
        embed.add_field(name="Done", value="Message Tags are now " +
                        tag_messages[str(ctx.guild.id)], inline=True)
        await ctx.send(embed=embed)

    @command(name="changepref", aliases=["changeprefix"], help="changes the prefix to the appended string")
    async def change_prefix(self, ctx, *args):
        prefix = "".join(args)
        if ctx.guild.id == int(os.environ['PUBLIC_BOT_SERVER']):
            embed = Embed(title="Status",
                          colour=0xff0000,
                          timestamp=datetime.utcnow())
            embed.add_field(
                name="Error", value="Prefix changes are not allowed on this server!", inline=True)
            await ctx.send(embed=embed)
        else:
            if ctx.author != ctx.guild.owner:
                embed = Embed(title="Status",
                              colour=0xff0000,
                              timestamp=datetime.utcnow())
                embed.add_field(
                    name="Error", value="Only server owner can change the prefix!", inline=True)
                await ctx.send(embed=embed)
                return
            if (prefix != ""):
                with open('./data/prefixes.json', 'r') as pref:
                    prefixes = json.load(pref)
                prefixes[str(ctx.guild.id)] = prefix
                embed = Embed(title="Status",
                              colour=0x00ff00,
                              timestamp=datetime.utcnow())
                embed.add_field(
                    name="Done", value="New Prefix is " + prefix, inline=True)
                await ctx.send(embed=embed)
                with open('./data/prefixes.json', 'w') as pref:
                    json.dump(prefixes, pref, indent=4)
            else:
                embed = Embed(title="Status",
                              colour=0xff0000,
                              timestamp=datetime.utcnow())
                embed.add_field(
                    name="Error", value="Blank prefixes not allowed!", inline=True)
                await ctx.send(embed=embed)
                
        
    @command(name="goodbyeForever!", aliases=["leaveThisServer"], help="makes the bot to leave the server (only for server owner)")
    async def leave_this_server(self, ctx):
        if ctx.author != ctx.guild.owner:
            embed = Embed(title="Status",
                          colour=0xff0000,
                          timestamp=datetime.utcnow())
            embed.add_field(
                name="Error", value="Only server owner can use this command!", inline=True)
            await ctx.send(embed=embed)
            return
        else:
            async with ctx.typing():
                embed = discord.Embed(title="**GOOD BYE!**", description=f"""
                Had a great time in {ctx.guild.name}!
                Now it's time, I guess!
                To report any issues: https://github.com/code-chaser/dex/issues/new
                """, color=0x8e38ce, timestamp=datetime.utcnow())
                embed.set_image(
                    url="https://user-images.githubusercontent.com/63065397/156924332-3638cd0d-9cf9-4e08-b4de-6f20cedd921a.png")
                embed.set_author(
                    name="dex", url="https://github.com/code-chaser/dex/issues/new", icon_url=self.bot.user.avatar_url)
                embed.set_footer(text="made by codechaser",
                                icon_url="https://avatars.githubusercontent.com/u/63065397?v=4")
                embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
            guild=ctx.guild
            await ctx.guild.leave()
            with open('./data/tag_messages.json', 'r') as tag_:
                tag_messages = json.load(tag_)
            if str(guild.id) in tag_messages.keys():
                tag_messages.pop(str(guild.id))
            with open('./data/tag_messages.json', 'w') as tag_:
                json.dump(tag_messages, tag_, indent=4)
            with open('./data/prefixes.json', 'r') as pref:
                prefixes = json.load(pref)
            if str(guild.id) in prefixes.keys():
                prefixes.pop(str(guild.id))
            with open('./data/prefixes.json', 'w') as pref:
                json.dump(prefixes, pref, indent=4)
            
    @command(name="madeby?", help="shows the creator of the bot")
    async def madeby(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(title="Made by", description="""
            **codechaser#0647**
            **[GitHub](https://github.com/code-chaser)**
            """,
            color=0x8e38ce, timestamp=datetime.utcnow())
            embed.set_author(name="dex",
                            url="https://github.com/code-chaser/dex/", icon_url=self.bot.user.avatar_url)
            
            embed.set_thumbnail(url="https://avatars.githubusercontent.com/u/63065397?v=4")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ModSet(bot))
