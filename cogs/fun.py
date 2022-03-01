from typing import Optional
from datetime import datetime
from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    def get_quote():
        response = requests.get("https://zenquotes.io/api//random")
        quote_json = json.loads(response.text)
        quote = "\"" + quote_json[0]['q'] + "\" -" + quote_json[0]['a']
        return (quote)
    @command(name = "inspire", aliases = ["iquote"])
    async def send_quote(self, ctx):
        embed = Embed(title = "Quote",
                     colour = 0xFFD700,
                     timestamp = datetime.utcnow())
        embed.set_thumbnail(url = target.avatar_url)
        fields = [
            ("Name", str(target), True),
            ("ID", target.id, True),
            ("Is Bot?", target.bot, True),
            ("Top Role", target.top_role.mention, True),
            ("Status", str(target.status).title(), True),
            ("Activity", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'None'} {target.activity.name if target.activity else ''}", True),
            ("Joined Discord at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Joined this Server at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Boosted", bool(target.premium_since), True)
        ]
        for n, v, i in fields:
            embed.add_field(name=n,value=v,inline=i)
        await ctx.send(embed=embed)

    @command(name = "serverinfo", aliases = ["si","guildinfo","gi"])
    async def server_info(self, ctx):
        embed = Embed(title = "Server Information",
                     colour = ctx.guild.owner.colour,
                     timestamp = datetime.utcnow())
        embed.set_thumbnail(url = ctx.guild.icon_url)

        statuses = [
            len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
            len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))
        ]
        
        fields = [
            ("Title", str(ctx.guild), True),
            ("ID", ctx.guild.id, True),
            ("Owner", str(ctx.guild.owner), True),
            ("Region", ctx.guild.region, True),
            ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Members", len(ctx.guild.members),True),
            ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
            ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
            ("Banned Members", len(await ctx.guild.bans()), True),
            ("Members' status", ":green_circle: " + str(statuses[0]) + " :orange_circle: " + str(statuses[1]) + " :red_circle: " + str(statuses[2]) + " :white_circle: " + str(statuses[3]), True),
            ("Text Channels", len(ctx.guild.text_channels), True),
            ("Voice Channels", len(ctx.guild.voice_channels), True),
            ("Categories", len(ctx.guild.categories), True),
            ("Roles", len(ctx.guild.roles), True),
            ("Invites", len(await ctx.guild.invites()), True),
            ("\u200b", "\u200b", True)
        ]
        for n, v, i in fields:
            embed.add_field(name=n,value=v,inline=i)
        await ctx.send(embed=embed)
        


def setup(bot):
    bot.add_cog(Info(bot))