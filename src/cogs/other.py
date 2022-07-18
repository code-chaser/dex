import discord
import aiohttp
from datetime import datetime
from discord.ext import commands


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_covid19_details(self):
        API_URL = "https://api.covid19api.com/summary"
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                data_json = await resp.json()
                return (data_json)

    @commands.command(name="covid19", help="sends COVID-19 stats of the given country (global stats if country == null)")
    async def covid19_command(self, ctx, *args):
        countr = ""
        for arg in args:
            countr += arg + " "
        size = len(countr)
        country = countr[:size - 1]
        original = country
        found = False
        stats = await self.get_covid19_details()
        if country:
            for k in stats["Countries"]:
                if ((k["CountryCode"]).lower() == country.lower()) or ((k["Country"]).lower() == country.lower()):
                    embed = discord.Embed(
                        title=(k["Country"]).title(),
                        description="COVID-19 Statistics",
                        colour=0xff0000,
                        timestamp=datetime.utcnow()
                    )
                    flag_url = "https://flagcdn.com/w640/" + \
                        str(k["CountryCode"]).lower() + ".jpg"
                    embed.set_thumbnail(url=flag_url)
                    fields = [
                        ("New Confirmed Cases", k["NewConfirmed"], True),
                        ("Total Confirmed Cases", k["TotalConfirmed"], True),
                        ("Country Code", k["CountryCode"], True),
                        ("New Deaths", k["NewDeaths"], True),
                        ("Total Deaths", k["TotalDeaths"], True),
                        ("Report Time (UTC)", "Date: " +
                         k["Date"][0:10] + " & Time: " + k["Date"][11:19], True),
                    ]
                    for n, v, i in fields:
                        embed.add_field(name=n, value=v, inline=i)
                    await ctx.send(reference=ctx.message, embed=embed)
                    found = True
        else:
            k = stats["Global"]
            embed = discord.Embed(
                title="Global",
                description="COVID-19 Statistics",
                colour=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(
                url="https://user-images.githubusercontent.com/63065397/156144079-6f90504d-ad48-4f2e-bec5-bae31cebd858.png"
            )
            fields = [
                ("New Confirmed Cases", k["NewConfirmed"], True),
                ("Total Confirmed Cases", k["TotalConfirmed"], True),
                ("New Deaths", k["NewDeaths"], True),
                ("Total Deaths", k["TotalDeaths"], True),
            ]
            for n, v, i in fields:
                embed.add_field(name=n, value=v, inline=i)
            await ctx.send(reference=ctx.message, embed=embed)
            found = True
        if not found:
            embed = discord.Embed(
                title="Error",
                description="Country Not Found",
                colour=0xff0000
            )
            embed.add_field(name="Given Country Name",
                            value=original, inline=True)
            await ctx.send(reference=ctx.message, embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="ping", aliases=["latency"], help="shows the latency of the bot")
    async def ping_command(self, ctx):
        async with ctx.typing():
            ping = round(self.bot.latency * 1000, 1)
            high = 400
            low = 30
            red = min((ping)/high, 1)
            green = 1-red
            if ping >= high:
                red = 1
                green = 0
            if ping <= low:
                red = 0
                green = 1
            embed = discord.Embed(
                title="Ping",
                description="**"+str(ping)+"ms**",
                colour=discord.Color.from_rgb(int(red*255), int(green*255), 0),
                timestamp=datetime.utcnow()
            )
        await ctx.send(reference=ctx.message, embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Other(bot))
