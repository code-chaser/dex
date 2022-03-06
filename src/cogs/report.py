import os

from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog


class Report(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        member_count = len(list(filter(lambda m: not m.bot, self.bot.users)))
        bot_count = len(list(filter(lambda m: m.bot, self.bot.users)))

        channel = self.bot.get_channel(int(os.environ["CONSOLE_CHANNEL_ID"]))
        embed = Embed(title="Status", colour=0x0023DD, timestamp=datetime.utcnow())
        fields = [
            ("Servers", str(len(self.bot.guilds)), True),
            ("Total Members", str(member_count), True),
            ("Total Bots", str(bot_count), True),
        ]

        for n, v, i in fields:
            embed.add_field(name=n, value=v, inline=i)
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        await channel.send(embed=embed)

        for target in self.bot.guilds:

            embed = Embed(title="Server Information", colour=target.owner.colour, timestamp=datetime.utcnow())
            embed.set_thumbnail(url=target.icon_url)
            statuses = [
                len(list(filter(lambda m: str(m.status) == "online", target.members))),
                len(list(filter(lambda m: str(m.status) == "idle", target.members))),
                len(list(filter(lambda m: str(m.status) == "dnd", target.members))),
                len(list(filter(lambda m: str(m.status) == "offline", target.members))),
            ]

            fields = [
                ("Title", str(target), True),
                ("ID", target.id, True),
                ("Owner", str(target.owner), True),
                ("Region", target.region, True),
                ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                ("Members", len(target.members), True),
                ("Humans", len(list(filter(lambda m: not m.bot, target.members))), True),
                ("Bots", len(list(filter(lambda m: m.bot, target.members))), True),
                ("Banned Members", len(await target.bans()), True),
                (
                    "Members' status",
                    ":green_circle: "
                    + str(statuses[0])
                    + " :orange_circle: "
                    + str(statuses[1])
                    + " :red_circle: "
                    + str(statuses[2])
                    + " :white_circle: "
                    + str(statuses[3]),
                    True,
                ),
                ("Text Channels", len(target.text_channels), True),
                ("Voice Channels", len(target.voice_channels), True),
                ("Categories", len(target.categories), True),
                ("Roles", len(target.roles), True),
                ("Invites", len(await target.invites()), True),
                ("\u200b", "\u200b", True),
            ]
            for n, v, i in fields:
                embed.add_field(name=n, value=v, inline=i)

            channel = self.bot.get_channel(int(os.environ["CONSOLE_CHANNEL_ID"]))

            await channel.send(embed=embed)

    @Cog.listener()
    async def on_message(self, message):
        target = message.author
        if target == self.bot.user:
            return

        embed = Embed(title="Message Information", colour=target.colour, timestamp=message.created_at)
        embed.set_thumbnail(url=target.avatar_url)
        embed.set_author(name=str(target), icon_url=target.avatar_url)
        embed.add_field(name="Message", value=message.content, inline=False)

        channel = self.bot.get_channel(int(os.environ["USAGE_HISTORY_CHANNEL_ID"]))
        await channel.send(embed=embed)

        embed = Embed(title="Message Information", colour=target.colour, timestamp=message.created_at)
        embed.set_thumbnail(url=message.guild.icon_url)
        fields = [
            ("Sent Time", message.created_at, True),
            ("Message ID", message.id, True),
            ("Channel", message.channel.name, True),
            ("Channel ID", message.channel.id, True),
            ("Server", message.guild.name, True),
            ("Server ID", message.guild.id, True),
            ("Author", str(target), True),
            ("Author ID", target.id, True),
            ("Author is Bot", target.bot, True),
            ("Author Top Role", str(target.top_role), True),
            ("Author Status", str(target.status).title(), True),
            (
                "Author Activity",
                f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'None'} {target.activity.name if target.activity else ''}",
                True,
            ),
            ("Author Joined Discord at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Author Joined that Server at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
            ("Author Boosted", bool(target.premium_since), True),
        ]
        for n, v, i in fields:
            embed.add_field(name=n, value=v, inline=i)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Report(bot))
