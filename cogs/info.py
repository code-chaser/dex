from typing import Optional
from datetime import datetime
from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command

class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name = "userinfo", aliases = ["ui","memberinfo","mi"])
    async def user_info(self, ctx, target: Optional[Member]):
        target = target or ctx.author
        embed = Embed(title = "User Information",
                     colour = target.colour,
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
            ("Boosted", bool(target.premium_since),True)
        ]
        for n, v, i in fields:
            embed.add_field(name=n,value=v,inline=i)
        await ctx.send(embed=embed)

    @command(name = "serverinfo", aliases = ["si","guildinfo","gi"])
    async def server_info(self, ctx):
        pass
        


def setup(bot):
    bot.add_cog(Info(bot))