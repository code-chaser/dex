import discord
import aiohttp
from typing import Optional
from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from pytz import timezone
from timezonefinder import TimezoneFinder
from datetime import datetime
from datetime import timedelta
from discord.ext import commands


class Other(commands.Cog):

    default_lat = 12.992855
    default_lng = 77.718837

    day_chaughadiya = [
        ["Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg"],
        ["Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit"],
        ["Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog"],
        ["Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh"],
        ["Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal", "Shubh"],
        ["Char", "Labh", "Amrit", "Kaal", "Shubh", "Rog", "Udveg", "Char"],
        ["Kaal", "Shubh", "Rog", "Udveg", "Char", "Labh", "Amrit", "Kaal"]
    ]

    night_chaughadiya = [
        ["Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh"],
        ["Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char"],
        ["Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal"],
        ["Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg"],
        ["Amrit", "Char", "Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit"],
        ["Rog", "Kaal", "Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog"],
        ["Labh", "Udveg", "Shubh", "Amrit", "Char", "Rog", "Kaal", "Labh"]
    ]

    time_dict = {"Udveg": -1, "Char": 0, "Labh": 1,
                 "Amrit": 1, "Kaal": -1, "Shubh": 1, "Rog": -1}

    week_days_number = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2,
                        'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6}
    # ----------------------------------------------------------------------------------------------------------------------

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

    async def get_suntime(self, lat, lng, date):
        # parse date
        date = date.split("-")
        date = date[2] + "-" + date[1] + "-" + date[0]
        API_URL = "https://api.sunrise-sunset.org/json?lat=" + \
            str(lat) + "&lng=" + str(lng) + "&date=" + date
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                data_json = await resp.json()
                return (data_json)

    @commands.command(name="suntime", help="shows the sunrise and sunset time of the given location")
    async def suntime_command(self, ctx, *args):
        lat = self.default_lat
        lng = self.default_lng
        date = datetime.now(timezone('Asia/Kolkata')).strftime("%d-%m-%Y")

        if len(args) == 1:
            date = args[0]
        elif len(args) == 3:
            lat = args[0]
            lng = args[1]
            date = args[2]

        async with ctx.typing():
            suntime = await self.get_suntime(lat, lng, date)
            if suntime["status"] == "OK":
                sunrise = suntime["results"]["sunrise"]
                sunset = suntime["results"]["sunset"]
                tf = TimezoneFinder()
                timezone = tf.timezone_at(lng=lng, lat=lat)
                embed = discord.Embed(
                    color=0xffd700,
                    description="**Sunrise Time**: " + sunrise + "\n**Sunset Time**: " + sunset,
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text="Timezone: UTC")
            else:
                embed = discord.Embed(
                    color=0xff0000,
                )
                embed.set_author(name="Unknown Error Occured!")
        await ctx.send(reference=ctx.message, embed=embed)
        return

    @commands.command(name="chaughadiya", help="shows the chaughadiya of the given location")
    async def chaughadiya_command(self, ctx, *args):
        lat = self.default_lat
        lng = self.default_lng
        date = datetime.now(timezone('Asia/Kolkata')).strftime("%d-%m-%Y")

        if len(args) == 1:
            date = args[0]
        elif len(args) == 3:
            lat = args[0]
            lng = args[1]
            date = args[2]

        async with ctx.typing():
            suntime = await self.get_suntime(lat, lng, date)
            if suntime["status"] == "OK":
                sunrise = suntime["results"]["sunrise"]
                sunset = suntime["results"]["sunset"]
                # convert to GMT + 5:30
                sunrise = datetime.strptime(sunrise, "%I:%M:%S %p")
                sunrise = sunrise + timedelta(hours=5, minutes=30)
                sunrise = sunrise.strftime("%H:%M:%S")
                sunset = datetime.strptime(sunset, "%I:%M:%S %p")
                sunset = sunset + timedelta(hours=5, minutes=30)
                sunset = sunset.strftime("%H:%M:%S")
                # get the difference and divide it into 8 parts
                sunrise = datetime.strptime(sunrise, "%H:%M:%S")
                sunset = datetime.strptime(sunset, "%H:%M:%S")
                diff = sunset - sunrise
                diff = diff / 8
                # get the today's day of the week for IST
                target_date = datetime.strptime(date, "%d-%m-%Y")
                target_date = target_date.strftime("%A")
                # get the chaughadiya for the day
                day_chaughadiya = self.day_chaughadiya[self.week_days_number[target_date]]
                # get the chaughadiya for the night
                night_chaughadiya = self.night_chaughadiya[self.week_days_number[target_date]]

                day_chaughadiya_string = ""
                for i in range(8):
                    day_chaughadiya_string += (sunrise + diff*i).strftime("%H:%M:%S") + " to " + \
                        (sunrise + diff*(i+1)).strftime("%H:%M:%S") + \
                        " - " + day_chaughadiya[i] + "\n"
                night_chaughadiya_string = ""
                for i in range(8):
                    night_chaughadiya_string += (sunset + diff*i).strftime("%H:%M:%S") + " to " + \
                        (sunset + diff*(i+1)).strftime("%H:%M:%S") + \
                        " - " + night_chaughadiya[i] + "\n"
                day_embed = discord.Embed(
                    color=0xffd700,
                    description="**Sunrise Time**: " + sunrise.strftime(
                        "%I:%M:%S %p") + "\n**Sunset Time**: " + sunset.strftime("%I:%M:%S %p") + "\n```\n" + day_chaughadiya_string + "```",
                )
                night_embed = discord.Embed(
                    color=0x0000ff,
                    description="**Sunset Time**: " + sunset.strftime("%I:%M:%S %p") + "\n**Sunrise Time**: " + sunrise.strftime(
                        "%I:%M:%S %p") + "\n```\n" + night_chaughadiya_string + "```",
                )
                embed_list = [day_embed, night_embed]
            else:
                embed = discord.Embed(
                    color=0xff0000,
                )
                embed.set_author(name="Unknown Error Occured!")
                embed_list = [embed]
        for embed in embed_list:
            await ctx.send(reference=ctx.message, embed=embed)
        return

    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Other(bot))
