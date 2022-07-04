import discord
import aiohttp
import datetime
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
                                      timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed)
            return
        async with ctx.typing():
            embed = discord.Embed(title=username,
                                  description=(handle["result"][0]["firstName"] if "firstName" in handle["result"][0] else "") + " " + (
                                      handle["result"][0]["lastName"] if "lastName" in handle["result"][0] else ""),
                                  colour=self.cf_red if handle["result"][0]["maxRating"] >= 2400 else self.cf_orange if handle["result"][0]["maxRating"] >= 2200 else self.cf_violet if handle["result"][0]["maxRating"] >= 1900 else self.cf_blue if handle[
                                      "result"][0]["maxRating"] >= 1600 else self.cf_cyan if handle["result"][0]["maxRating"] >= 1400 else self.cf_green if handle["result"][0]["maxRating"] >= 1200 else self.cf_gray,
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="City", value=handle["result"][0]["city"]
                            if "city" in handle["result"][0] else "Unknown", inline=True)
            embed.add_field(name="Country", value=handle["result"][0]["country"]
                            if "country" in handle["result"][0] else "Unknown", inline=True)
            embed.add_field(
                name="Friend of", value=handle["result"][0]["friendOfCount"], inline=True)
            embed.add_field(name="Max Rating",
                            value=handle["result"][0]["maxRating"], inline=True)
            embed.add_field(name="Max Rank",
                            value=handle["result"][0]["maxRank"], inline=True)
            embed.add_field(name="Organization", value=handle["result"][0]["organization"]
                            if handle["result"][0]["organization"] != "" else "Unknown", inline=True)
            embed.add_field(
                name="Rating", value=handle["result"][0]["rating"], inline=True)
            embed.add_field(
                name="Rank", value=handle["result"][0]["rank"], inline=True)
            embed.add_field(name="Last Online", value=datetime.datetime.utcfromtimestamp(
                handle["result"][0]["lastOnlineTimeSeconds"]).strftime('%Y-%m-%d %H:%M:%S'), inline=True)
            embed.set_thumbnail(url=handle["result"][0]["avatar"])
        await ctx.reply(embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Codeforces(bot))
