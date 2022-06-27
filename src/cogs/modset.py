import discord
import os
from typing import Optional
from datetime import datetime
from discord.ext import commands


class ModSet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="modset", aliases=["mset", "modsettings"])
    async def modset(self, ctx, target: Optional[discord.Member]):
        pass

    @commands.command(name="tags", aliases=["tagging", "msgtag"], help="toggles message tags")
    async def tags_command(self, ctx, switch: Optional[str]):
        tag_switch = self.bot.DATABASE['guilds'][str(
            ctx.guild.id)]['tag_messages']
        if switch is None:
            if tag_switch == "off":
                tag_switch = "on"
            else:
                tag_switch = "off"
        elif switch == "0" or switch.lower() == "off":
            tag_switch = "off"
        elif switch == "1" or switch.lower() == "on":
            tag_switch = "on"

        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Status",
                    colour=0xff0000,
                    timestamp=datetime.utcnow()
                )
                embed.add_field(
                    name="Error",
                    value="Invalid value provided",
                    inline=True
                )
            await ctx.send(embed=embed)
            return

        await self.bot.DB_CONNECTION.execute('UPDATE guilds SET tag_messages = \'' + tag_switch +
                                             '\' WHERE guild_id = \'' + str(ctx.guild.id) + '\';')
        self.bot.DATABASE['guilds'][str(
            ctx.guild.id)]['tag_messages'] = tag_switch
        async with ctx.typing():
            embed = discord.Embed(
                title="Status",
                colour=0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="Done",
                value="Message Tags are now " + tag_switch,
                inline=True
            )
        await ctx.send(embed=embed)

    @commands.command(name="changepref", aliases=["changeprefix"], help="changes the prefix to the appended string")
    async def changeprefix_command(self, ctx, *args):
        prefix = "".join(args)
        if ctx.guild.id == int(os.environ['DEX_PUBLIC_BOT_SERVER']):
            embed = discord.Embed(title="Status",
                                  description="Permission Denied",
                                  colour=0xff0000,
                                  timestamp=datetime.utcnow())
            embed.add_field(
                name="Error", value="Prefix changes are not allowed on this server!", inline=True)
            await ctx.send(embed=embed)
        else:
            if ctx.author != ctx.guild.owner:
                embed = discord.Embed(title="Status",
                                      description="Permission Denied",
                                      colour=0xff0000,
                                      timestamp=datetime.utcnow())
                embed.add_field(
                    name="Error", value="Only server owner can change the prefix!", inline=True)
                await ctx.send(embed=embed)
                return
            if (prefix != "") and (len(prefix) <= 27):
                prefix += " "
                await self.bot.DB_CONNECTION.execute("UPDATE guilds SET prefix = \'"+prefix +
                                                     "\' WHERE guild_id = \'"+str(ctx.guild.id)+"\';")
                self.bot.DATABASE['guilds'][str(
                    ctx.guild.id)]['prefix'] = prefix
                embed = discord.Embed(title="Status",
                                      colour=0x00ff00,
                                      timestamp=datetime.utcnow())
                embed.add_field(
                    name="Done", value="New Prefix is `" + prefix + "`", inline=True)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Status",
                                      colour=0xff0000,
                                      timestamp=datetime.utcnow())
                embed.add_field(
                    name="Error", value="prefix length must be between (1 - 27)", inline=True)
                await ctx.send(embed=embed)

    @commands.command(name="prefixspace", aliases=["prefspace"], help="toggles the trailing space in the prefix")
    async def prefixspace_command(self, ctx, switch: Optional[str]):
        if ctx.guild.id == int(os.environ['DEX_PUBLIC_BOT_SERVER']):
            embed = discord.Embed(title="Status",
                                  description="Permission Denied",
                                  colour=0xff0000,
                                  timestamp=datetime.utcnow())
            embed.add_field(
                name="Error", value="Prefix changes are not allowed on this server!", inline=True)
            await ctx.send(embed=embed)
            return
        if ctx.author != ctx.guild.owner:
            embed = discord.Embed(title="Status",
                                  description="Permission Denied",
                                  colour=0xff0000,
                                  timestamp=datetime.utcnow())
            embed.add_field(
                name="Error", value="Only server owner can use this command!", inline=True)
            await ctx.send(embed=embed)
            return
        prefix_space_switch = 'on' if self.bot.DATABASE['guilds'][str(
            ctx.guild.id)]['prefix'][-1] == ' ' else 'off'
        if switch is None:
            if prefix_space_switch == 'on':
                prefix_space_switch = 'off'
            else:
                prefix_space_switch = 'on'
        elif switch == "0" or switch.lower() == "off":
            prefix_space_switch = "off"
        elif switch == "1" or switch.lower() == "on":
            prefix_space_switch = "on"
        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Status",
                    colour=0xff0000,
                    timestamp=datetime.utcnow()
                )
                embed.add_field(
                    name="Error",
                    value="Invalid value provided",
                    inline=True
                )
            await ctx.send(embed=embed)
            return

        prefix = self.bot.DATABASE['guilds'][str(ctx.guild.id)]['prefix'] = self.bot.DATABASE['guilds'][str(
            ctx.guild.id)]['prefix'].strip() + (' ' if prefix_space_switch == 'on' else '')
        await self.bot.DB_CONNECTION.execute("UPDATE guilds SET prefix = \'" + prefix +
                                             "\' WHERE guild_id = \'" + str(ctx.guild.id) + "\';")

        async with ctx.typing():
            embed = discord.Embed(
                title="Status",
                colour=0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="Done",
                value="Prefix Space is now " + prefix_space_switch,
                inline=False
            )
            embed.add_field(
                name="Prefix",
                value="`" + prefix + "`",
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(name="goodbye!", aliases=["leaveThisServer"], help="makes the bot to leave the server (only for server owner)")
    async def goodbye_command(self, ctx):
        if ctx.author != ctx.guild.owner:
            embed = discord.Embed(title="Status",
                                  description="Permission Denied",
                                  colour=0xff0000,
                                  timestamp=datetime.utcnow())
            embed.add_field(
                name="Error", value="Only server owner can use this command!", inline=True)
            await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                embed = discord.Embed(title="**GOOD BYE!**", description=f"""
                Had a great time in {ctx.guild.name}!
                Now it's time, I guess!
                Report any issues: [Here](https://github.com/code-chaser/dex/issues/new)
                """, color=0x8e38ce, timestamp=datetime.utcnow())
                embed.set_image(
                    url="https://user-images.githubusercontent.com/63065397/156924332-3638cd0d-9cf9-4e08-b4de-6f20cedd921a.png")
                embed.set_author(
                    name="dex", url="https://github.com/code-chaser/dex/issues/new", icon_url=self.bot.user.avatar_url)
                embed.set_footer(text="made by codechaser",
                                 icon_url="https://avatars.githubusercontent.com/u/63065397?v=4")
                embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.send(embed=embed)
            guild = ctx.guild
            await ctx.guild.leave()
        return

    @commands.command(name="madeby?", help="shows the creator of the bot")
    async def madeby_command(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(title="Made by", description="""
            **codechaser#0647**
            **[GitHub](https://github.com/code-chaser)**
            """,
                                  color=0x8e38ce, timestamp=datetime.utcnow())
            embed.set_author(name="dex",
                             url="https://github.com/code-chaser/dex/", icon_url=self.bot.user.avatar_url)

            embed.set_thumbnail(
                url="https://avatars.githubusercontent.com/u/63065397?v=4")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ModSet(bot))
