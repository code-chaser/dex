import requests
import json
from typing import Optional
from datetime import datetime
from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
    def get_iquote(self):
        response = requests.get("https://zenquotes.io/api//random")
        quote_json = json.loads(response.text)
        quote = "\"" + quote_json[0]['q'] + "\" -" + quote_json[0]['a']
        return (quote_json)
    def get_nasa(self):
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key=KljLJ0j9I3khrq8LbWjYsHncz680WFJabuRLkhIv")
        response_json = json.loads(response.text)
        return response_json
    @command(name = "inspire", aliases = ["iquote"])
    async def send_iquote(self, ctx):
        embed = Embed(title = "Inspirational Quote",
                     colour = ctx.author.colour,
                     timestamp = datetime.utcnow())
        iquote = self.get_iquote()
        embed.add_field(name="Quote", value=iquote[0]['q'], inline=False)
        embed.add_field(name="Author", value=iquote[0]['a'] , inline=False)
        await ctx.send(embed=embed)

    @command(name = "nasapic", aliases = ["nasapicotd","astropic","astropicotd"])
    async def send_nasa_pic_otd(self, ctx):
        embed = Embed(title = "NASA",
                     description = "Picture of the day",
                     colour = ctx.author.colour,
                     timestamp = datetime.utcnow())
        nasa_api = self.get_nasa()
        embed.set_image(url=nasa_api["url"])
        embed.add_field(name="Date", value=nasa_api["date"], inline=False)
        embed.add_field(name="Image Title", value=nasa_api["title"] , inline=False)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Fun(bot))