import discord
from typing import Optional
from datetime import datetime
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="userinfo", aliases=["ui", "memberinfo", "mi"], help="shows user information")
    async def userinfo_command(self, ctx, target: Optional[discord.Member]):
        target = target or ctx.author
        embed = discord.Embed(title="User Information",
                      colour=target.colour,
                      timestamp=datetime.utcnow())
        embed.set_thumbnail(url=target.avatar_url)
        fields = [
            ("Name", str(target), True),
            ("ID", target.id, True),
            ("Is Bot?", target.bot, True),
            ("Top Role", target.top_role.mention, True),
            ("Status", str(target.status).title(), True),
            ("Activity",
             f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'None'} {target.activity.name if target.activity else ''}", True),
            ("Joined Discord at", target.created_at.strftime(
                "%d/%m/%Y %H:%M:%S"), True),
            ("Joined this Server at", target.joined_at.strftime(
                "%d/%m/%Y %H:%M:%S"), True),
            ("Boosted", bool(target.premium_since), True)
        ]
        for n, v, i in fields:
            embed.add_field(name=n, value=v, inline=i)
        await ctx.send(reference=ctx.message, embed=embed)

    @commands.command(name="serverinfo", aliases=["si", "guildinfo", "gi"], help="shows server information")
    async def serverinfo_command(self, ctx, target: Optional[discord.Guild]):
        flag = True
        if(target):
            flag = False
            for g in self.bot.guilds:
                if g.id == target.id:
                    flag = True
        target = target or ctx.guild
        embed = discord.Embed(title="Server Information",
                      colour=ctx.guild.owner.colour,
                      timestamp=datetime.utcnow())
        if flag == False:
            embed.add_field(
                name="Error", value="Dex doesn't have access to the requested server.", inline=True)
        else:
            embed.set_thumbnail(url=target.icon_url)

            fields = []
            try:
                statuses = [
                    len(list(filter(lambda m: str(m.status) == "online", target.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", target.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", target.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", target.members)))
                ]
                fields = [
                    ('Title', str(target), True),
                    ('ID', target.id, True),
                    ('Owner', str(target.owner), True),
                    ('Region', target.region, True),
                    ('Created at', target.created_at.strftime(
                        '%d/%m/%Y %H:%M:%S'), True),
                    ('Members', len(target.members), True),
                    ('Humans', len(list(filter(lambda m: not m.bot, target.members))), True),
                    ('Bots', len(list(filter(lambda m: m.bot, target.members))), True),
                    ('Banned Members', len(await target.bans()), True),
                    ("Members' status", ':green_circle: ' + str(statuses[0]) + ' :orange_circle: ' + str(
                        statuses[1]) + ' :red_circle: ' + str(statuses[2]) + ' :white_circle: ' + str(statuses[3]), True),
                    ('Text Channels', len(target.text_channels), True),
                    ('Voice Channels', len(target.voice_channels), True),
                    ('Categories', len(target.categories), True),
                    ('Roles', len(target.roles), True),
                    ('Invites', len(await target.invites()), True),
                    ('\u200b', '\u200b', True)
                ]
            except discord.errors.Forbidden:
                fields = [
                    ('Title', str(target), True),
                    ('ID', target.id, True)
                ]
            for n, v, i in fields:
                embed.add_field(name=n, value=v, inline=i)
        await ctx.send(reference=ctx.message, embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
