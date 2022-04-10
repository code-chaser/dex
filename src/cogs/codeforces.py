import discord
import aiohttp
import json
import os
import datetime
import typing
from discord.ext import commands
from psycopg2 import Timestamp


class Codeforces(commands.Cog):
    cf_red = 0xff0000 # 2400+
    cf_orange = 0xff8c00 # 2200 - 2399
    cf_violet = 0xb200aa # 1900 - 2199
    cf_blue = 0x0000ff # 1600 - 1899
    cf_cyan = 0x03a89e # 1400 - 1599
    cf_green = 0x008000 # 1200 - 1399
    cf_gray = 0x808080 # 0 - 1199
    def __init__(self, bot):
        self.bot = bot
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_user(self, username):
        API_URL = "https://codeforces.com/api/user.info?handles=" + username + ";"
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                user_json = await resp.json()
                return (user_json)

    @commands.command(name="cf-handle", aliases=["cf-user"], help="shows details of the requested codeforces handle")
    async def send_user(self, ctx, username):
        handle=await self.get_user(username)
        if handle["status"]=="FAILED":
            async with ctx.typing():
                embed = discord.Embed(title="Error",
                                    description=handle["comment"],
                                    colour=0xff0000,
                                    timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return
        async with ctx.typing():
            embed = discord.Embed(title=username,
                                description=(handle["result"][0]["firstName"] if "firstName" in handle["result"][0] else "") + " " + (handle["result"][0]["lastName"] if "lastName" in handle["result"][0] else ""),
                                colour=self.cf_red if handle["result"][0]["maxRating"]>=2400 else self.cf_orange if handle["result"][0]["maxRating"]>=2200 else self.cf_violet if handle["result"][0]["maxRating"]>=1900 else self.cf_blue if handle["result"][0]["maxRating"]>=1600 else self.cf_cyan if handle["result"][0]["maxRating"]>=1400 else self.cf_green if handle["result"][0]["maxRating"]>=1200 else self.cf_gray,
                                timestamp=datetime.datetime.utcnow())
            embed.add_field(name="City", value=handle["result"][0]["city"] if "city" in handle["result"][0] else "Unknown", inline=True)
            embed.add_field(name="Country", value=handle["result"][0]["country"] if "country" in handle["result"][0] else "Unknown", inline=True)
            embed.add_field(name="Friend of", value=handle["result"][0]["friendOfCount"], inline=True)
            embed.add_field(name="Max Rating", value=handle["result"][0]["maxRating"], inline=True)
            embed.add_field(name="Max Rank", value=handle["result"][0]["maxRank"], inline=True)
            embed.add_field(name="Organization", value=handle["result"][0]["organization"] if handle["result"][0]["organization"]!="" else "Unknown", inline=True)
            embed.add_field(name="Rating", value=handle["result"][0]["rating"], inline=True)
            embed.add_field(name="Rank", value=handle["result"][0]["rank"], inline=True)
            embed.add_field(name="Last Online", value=datetime.datetime.utcfromtimestamp(handle["result"][0]["lastOnlineTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S'), inline=True)
            embed.set_thumbnail(url=handle["result"][0]["avatar"])
        await ctx.send(embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------
    
    # async def get_nasa(self):
    #     API_URL = "https://api.nasa.gov/planetary/apod?api_key=" + \
    #         str(os.getenv('NASA_API_KEY'))
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(API_URL) as resp:
    #             data_json = await resp.json()
    #             return (data_json)

    # @commands.command(name="apod", aliases=["napod", "astropic", "astropicotd"], help="sends astronomy pic of the day from NASA")
    # async def send_nasa_pic_otd(self, ctx):
    #     embed = discord.Embed(title="NASA",
    #                           description="Picture of the day",
    #                           colour=0x0B3D91,
    #                           timestamp=datetime.datetime.utcnow())
    #     embed.set_thumbnail(
    #         url="https://user-images.githubusercontent.com/63065397/156291255-4af80382-836c-4801-8b4f-47da33ea36c5.png")
    #     embed.set_footer(text="updated daily at 05:00:00 UTC [00:00:00 ET]")
    #     nasa_api = await self.get_nasa()
    #     embed.set_image(url=nasa_api["url"])
    #     embed.add_field(name="Date", value=nasa_api["date"], inline=False)
    #     embed.add_field(name="Image Title",
    #                     value=nasa_api["title"], inline=False)
    #     await ctx.send(embed=embed)
    # # ----------------------------------------------------------------------------------------------------------------------

    # async def get_covid19_details(self):
    #     API_URL = "https://api.covid19api.com/summary"
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(API_URL) as resp:
    #             data_json = await resp.json()
    #             return (data_json)

    # @commands.command(name="covid19", help="sends COVID-19 stats of the given country (global stats if country == null)")
    # async def covid19_data(self, ctx, *args):
    #     countr = ""
    #     for arg in args:
    #         countr += arg + " "
    #     size = len(countr)
    #     country = countr[:size - 1]
    #     original = country
    #     found = False
    #     stats = await self.get_covid19_details()
    #     if country:
    #         for k in stats["Countries"]:
    #             if ((k["CountryCode"]).lower() == country.lower()) or ((k["Country"]).lower() == country.lower()):
    #                 embed = discord.Embed(
    #                     title=(k["Country"]).title(),
    #                     description="COVID-19 Statistics",
    #                     colour=0xff0000,
    #                     timestamp=datetime.datetime.utcnow()
    #                 )
    #                 flag_url = "https://flagcdn.com/w640/" + \
    #                     str(k["CountryCode"]).lower() + ".jpg"
    #                 embed.set_thumbnail(url=flag_url)
    #                 fields = [
    #                     ("New Confirmed Cases", k["NewConfirmed"], True),
    #                     ("Total Confirmed Cases", k["TotalConfirmed"], True),
    #                     ("Country Code", k["CountryCode"], True),
    #                     ("New Deaths", k["NewDeaths"], True),
    #                     ("Total Deaths", k["TotalDeaths"], True),
    #                     ("Report Time (UTC)", "Date: " +
    #                      k["Date"][0:10] + " & Time: " + k["Date"][11:19], True),
    #                 ]
    #                 for n, v, i in fields:
    #                     embed.add_field(name=n, value=v, inline=i)
    #                 await ctx.send(embed=embed)
    #                 found = True
    #     else:
    #         k = stats["Global"]
    #         embed = discord.Embed(
    #             title="Global",
    #             description="COVID-19 Statistics",
    #             colour=0xff0000,
    #             timestamp=datetime.datetime.utcnow()
    #         )
    #         embed.set_thumbnail(
    #             url="https://user-images.githubusercontent.com/63065397/156144079-6f90504d-ad48-4f2e-bec5-bae31cebd858.png"
    #         )
    #         fields = [
    #             ("New Confirmed Cases", k["NewConfirmed"], True),
    #             ("Total Confirmed Cases", k["TotalConfirmed"], True),
    #             ("New Deaths", k["NewDeaths"], True),
    #             ("Total Deaths", k["TotalDeaths"], True),
    #         ]
    #         for n, v, i in fields:
    #             embed.add_field(name=n, value=v, inline=i)
    #         await ctx.send(embed=embed)
    #         found = True
    #     if not found:
    #         embed = discord.Embed(
    #             title="Error",
    #             description="Country Not Found",
    #             colour=0xff0000
    #         )
    #         embed.add_field(name="Given Country Name",
    #                         value=original, inline=True)
    #         await ctx.send(embed=embed)
    # # ----------------------------------------------------------------------------------------------------------------------

    # async def get_meme(self):
    #     API_URL = "https://meme-api.herokuapp.com/gimme"
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(API_URL) as resp:
    #             data_json = await resp.json()
    #             return (data_json)

    # @commands.command(name="meme", aliases=["hehe"], help="sends a random meme")
    # async def send_meme(self, ctx):
    #     embed = discord.Embed(title="MEME",
    #                           colour=0xffee00,
    #                           timestamp=datetime.datetime.utcnow())
    #     meme = await self.get_meme()
    #     embed.add_field(name="Post Link", value=meme["postLink"], inline=True)
    #     embed.add_field(name="Author", value=meme["author"], inline=True)
    #     embed.add_field(name="Header", value=meme["title"], inline=False)
    #     embed.set_image(url=meme["url"])
    #     embed.set_thumbnail(
    #         url="https://user-images.githubusercontent.com/63065397/156142184-0675cfee-2863-41d7-bef8-87f600a713b0.png")
    #     await ctx.send(embed=embed)
    # # ----------------------------------------------------------------------------------------------------------------------

    # async def get_subreddit(self, subreddit):
    #     API_URL = str("https://www.reddit.com/r/" + subreddit + ".json")
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(API_URL) as resp:
    #             data_json = await resp.json()
    #             return (data_json)

    # @commands.command(name="reddit", aliases=["subreddit"], help="shows top headlines of the given subreddit")
    # async def send_subreddit(self, ctx, subreddit, number: typing.Optional[int]):
    #     data = await self.get_subreddit(subreddit)
    #     if ('message' in data.keys()):
    #         if data['message'] == "Not Found":
    #             embed = discord.Embed(
    #                 title="Status",
    #                 colour=0xff0000,
    #                 timestamp=datetime.datetime.utcnow()
    #             )
    #             embed.add_field(name="Error", value="Not Found", inline=True)
    #             embed.set_footer(text="given subreddit: "+subreddit)
    #             await ctx.send(embed=embed)
    #             return
    #         embed = discord.Embed(
    #             title="Error",
    #             description="API Request Fail",
    #             colour=0xff0000,
    #             timestamp=datetime.datetime.utcnow()
    #         )
    #         for key_i in data.keys():
    #             if key_i != 'message' and key_i != 'error':
    #                 new_key = key_i
    #         embed.add_field(name='Error Code', value=str(
    #             data['error']), inline=True)
    #         embed.add_field(name='Error Message', value=str(
    #             data['message']), inline=True)
    #         if new_key is not None:
    #             embed.add_field(name=new_key.title(), value=str(
    #                 data[new_key]), inline=True)
    #         embed.set_footer(text="given subreddit: "+subreddit)
    #         await ctx.send(embed=embed)
    #     else:
    #         embed = discord.Embed(title=str("/r/"+subreddit),
    #                               colour=0xff5700, timestamp=datetime.datetime.utcnow())
    #         embed.set_thumbnail(
    #             url="https://user-images.githubusercontent.com/63065397/156344382-821872f3-b6e3-46e7-b925-b5f1a0821da8.png")
    #         i = 1
    #         if number is None:
    #             number = 5
    #         for head in (data['data']['children']):
    #             embed.add_field(
    #                 name=str(i),
    #                 value=head['data']['title'][0:127] + "...",
    #                 inline=False
    #             )
    #             i += 1
    #             if i > number:
    #                 break
    #         if i <= number:
    #             embed.add_field(
    #                 name=str(i),
    #                 value="No more data could be received...",
    #                 inline=False
    #             )
    #         if number > 0:
    #             await ctx.send(embed=embed)
    #         return
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Codeforces(bot))
