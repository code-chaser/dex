import discord
import aiohttp
from datetime import datetime
from discord.ext import commands


class Codeforces(commands.Cog):
    cf_red = 0xff0000  # 2400+
    cf_orange = 0xff8c00  # 2200 - 2399
    cf_violet = 0xb200aa  # 1900 - 2199
    cf_blue = 0x0000ff  # 1600 - 1899
    cf_cyan = 0x03a89e  # 1400 - 1599
    cf_green = 0x008000  # 1200 - 1399
    cf_gray = 0x808080  # 0 - 1199

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
    async def cf_handle_command(self, ctx, username):
        handle = await self.get_user(username)
        if handle["status"] == "FAILED":
            async with ctx.typing():
                embed = discord.Embed(title="Error",
                                      description=handle["comment"],
                                      colour=0xff0000,
                                      timestamp=datetime.utcnow())
            await ctx.send(reference=ctx.message, embed=embed)
            return
        for res in handle["result"]:
            async with ctx.typing():
                max_rating_color = self.cf_gray
                if res["maxRating"] < 1200:
                    max_rating_color = self.cf_gray
                elif res["maxRating"] < 1400:
                    max_rating_color = self.cf_green
                elif res["maxRating"] < 1600:
                    max_rating_color = self.cf_cyan
                elif res["maxRating"] < 1900:
                    max_rating_color = self.cf_blue
                elif res["maxRating"] < 2100:
                    max_rating_color = self.cf_violet
                elif res["maxRating"] < 2400:
                    max_rating_color = self.cf_orange
                else:
                    max_rating_color = self.cf_red
                curr_rating_color = self.cf_gray
                if res["rating"] < 1200:
                    curr_rating_color = self.cf_gray
                elif res["rating"] < 1400:
                    curr_rating_color = self.cf_green
                elif res["rating"] < 1600:
                    curr_rating_color = self.cf_cyan
                elif res["rating"] < 1900:
                    curr_rating_color = self.cf_blue
                elif res["rating"] < 2100:
                    curr_rating_color = self.cf_violet
                elif res["rating"] < 2400:
                    curr_rating_color = self.cf_orange
                else:
                    curr_rating_color = self.cf_red
                embed = discord.Embed(title=username,
                                    description=(res["firstName"] if "firstName" in res else "") + " " + (
                                        res["lastName"] if "lastName" in res else ""),
                                    colour=max_rating_color,
                                    timestamp=datetime.utcnow())
                embed.add_field(name="City", value=res["city"]
                                if "city" in res else "Unknown", inline=True)
                embed.add_field(name="Country", value=res["country"]
                                if "country" in res else "Unknown", inline=True)
                embed.add_field(
                    name="Friend of", value=res["friendOfCount"], inline=True)
                embed.add_field(name="Max Rating",
                                value=res["maxRating"], inline=True)
                embed.add_field(name="Max Rank",
                                value=res["maxRank"], inline=True)
                embed.add_field(name="Organization", value=res["organization"]
                                if res["organization"] != "" else "Unknown", inline=True)
                embed.add_field(
                    name="Rating", value=res["rating"], inline=True)
                embed.add_field(
                    name="Rank", value=res["rank"], inline=True)
                embed.add_field(name="Last Online", value=datetime.utcfromtimestamp(
                    res["lastOnlineTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S'), inline=True)
                embed.set_thumbnail(url=res["avatar"])
            await ctx.send(reference=ctx.message, embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Codeforces(bot))
