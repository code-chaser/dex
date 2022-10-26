import difflib
import discord
import aiohttp
import os
from typing import Optional
from datetime import datetime
from discord.ext import commands
from gtts import gTTS, lang
from random import randint

class Fun(commands.Cog):
    trivia_categories = [
        {"id": 3, "title": "hunting", "clues_count": 0},
        {"id": 89, "title": "fiction", "clues_count": 75},
        {"id": 64, "title": "politics", "clues_count": 35},
        {"id": 7, "title": "governors", "clues_count": 36},
        {"id": 79, "title": "islands", "clues_count": 127},
        {"id": 19, "title": "weather", "clues_count": 121},
        {"id": 1, "title": "u.s. cities", "clues_count": 390},
        {"id": 44, "title": "crime \u0026 punishment", "clues_count": 44},
        {"id": 1970, "title": "california cities", "clues_count": 10},
        {"id": 35, "title": "current events", "clues_count": 55},
        {"id": 11, "title": "1960", "clues_count": 15},
        {"id": 43, "title": "egypt", "clues_count": 19},
        {"id": 61, "title": "mammals", "clues_count": 196},
        {"id": 8, "title": "4-word phrases", "clues_count": 5},
        {"id": 25, "title": "word play", "clues_count": 10},
        {"id": 26, "title": "canada", "clues_count": 21},
        {"id": 30, "title": "anatomy", "clues_count": 75},
        {"id": 68, "title": "australia", "clues_count": 33},
        {"id": 100, "title": "time", "clues_count": 70},
        {"id": 86, "title": "1965", "clues_count": 8},
        {"id": 15, "title": "india", "clues_count": 18},
        {"id": 24, "title": "1933", "clues_count": 15},
        {"id": 58, "title": "u.s. geography", "clues_count": 316},
        {"id": 88, "title": "music", "clues_count": 132},
        {"id": 40, "title": "easy math", "clues_count": 20},
        {"id": 41, "title": "food facts", "clues_count": 100},
        {"id": 110, "title": "cars", "clues_count": 46},
        {"id": 54, "title": "zoology", "clues_count": 215},
        {"id": 34, "title": "winter sports", "clues_count": 3},
        {"id": 27, "title": "movie trivia", "clues_count": 103},
        {"id": 5, "title": "automobiles", "clues_count": 52},
        {"id": 104, "title": "american revolution", "clues_count": 21},
        {"id": 93, "title": "gymnastics", "clues_count": 20},
        {"id": 10265, "title": "1980s bestsellers", "clues_count": 5},
        {"id": 70, "title": "scotland", "clues_count": 35},
        {"id": 10266, "title": "name the war", "clues_count": 5},
        {"id": 49, "title": "double meanings", "clues_count": 15},
        {"id": 51, "title": "rituals", "clues_count": 18},
        {"id": 38, "title": "asia", "clues_count": 34},
        {"id": 9, "title": "the olympics", "clues_count": 87},
        {"id": 91, "title": "number please", "clues_count": 25},
        {"id": 10267, "title": "sound technology", "clues_count": 5},
        {"id": 72, "title": "gangster movies", "clues_count": 5},
        {"id": 65, "title": "baseball", "clues_count": 131},
        {"id": 6701, "title": "coming to a clothes", "clues_count": 5},
        {"id": 81, "title": "vegetables", "clues_count": 2},
        {"id": 1972, "title": "june 1969", "clues_count": 5},
        {"id": 1975, "title": "world geography", "clues_count": 5},
    ]
    # ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, bot):
        self.bot = bot
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_iquote(self):
        API_URL = "https://zenquotes.io/api//random"
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                quote_json = await resp.json()
                return (quote_json)

    @commands.command(name="inspire", aliases=["iquote"], help="sends a random inspirational quote")
    async def inspire_command(self, ctx):
        embed = discord.Embed(title="Inspirational Quote",
                              colour=ctx.author.colour,
                              timestamp=datetime.utcnow())
        iquote = await self.get_iquote()
        embed.add_field(name="Quote", value=iquote[0]['q'], inline=False)
        embed.add_field(name="Author", value=iquote[0]['a'], inline=False)
        await ctx.send(reference=ctx.message, embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_nasa(self):
        API_URL = "https://api.nasa.gov/planetary/apod?api_key=" + \
            str(os.getenv('DEX_NASA_API_KEY'))
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                data_json = await resp.json()
                return (data_json)

    @commands.command(name="apod", aliases=["napod", "astropic", "astropicotd"], help="sends astronomy pic of the day from NASA")
    async def apod_command(self, ctx):
        embed = discord.Embed(title="NASA",
                              description="Picture of the day",
                              colour=0x0B3D91,
                              timestamp=datetime.utcnow())
        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/63065397/156291255-4af80382-836c-4801-8b4f-47da33ea36c5.png")
        embed.set_footer(text="updated daily at 05:00:00 UTC [00:00:00 ET]")
        nasa_api = await self.get_nasa()
        if nasa_api["media_type"] == "image":
            embed.set_image(url=nasa_api["url"])
        else:
            embed.add_field(name="Video Found", value=nasa_api["url"], inline=False)
        embed.set_image(url=nasa_api["url"])
        embed.add_field(name="Date", value=nasa_api["date"], inline=False)
        embed.add_field(name="Image Title",
                        value=nasa_api["title"], inline=False)
        await ctx.send(reference=ctx.message, embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_meme(self):
        API_URL = "https://meme-api.herokuapp.com/gimme"
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                data_json = await resp.json()
                return (data_json)

    @commands.command(name="meme", aliases=["hehe"], help="sends a random meme")
    async def meme_command(self, ctx):
        embed = discord.Embed(title="MEME",
                              colour=0xffee00,
                              timestamp=datetime.utcnow())
        meme = await self.get_meme()
        embed.add_field(name="Post Link", value=meme["postLink"], inline=True)
        embed.add_field(name="Author", value=meme["author"], inline=True)
        embed.add_field(name="Header", value=meme["title"], inline=False)
        embed.set_image(url=meme["url"])
        embed.set_thumbnail(
            url="https://user-images.githubusercontent.com/63065397/156142184-0675cfee-2863-41d7-bef8-87f600a713b0.png")
        await ctx.send(reference=ctx.message, embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_subreddit(self, subreddit):
        API_URL = str("https://www.reddit.com/r/" + subreddit + ".json")
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                data_json = await resp.json()
                return (data_json)

    @commands.command(name="reddit", aliases=["subreddit"], help="shows top headlines of the given subreddit")
    async def reddit_command(self, ctx, subreddit, number: Optional[int]):
        data = await self.get_subreddit(subreddit)
        if ('message' in data.keys()):
            if data['message'] == "Not Found":
                embed = discord.Embed(
                    title="Status",
                    colour=0xff0000,
                    timestamp=datetime.utcnow()
                )
                embed.add_field(name="Error", value="Not Found", inline=True)
                embed.set_footer(text="given subreddit: "+subreddit)
                await ctx.send(reference=ctx.message, embed=embed)
                return
            embed = discord.Embed(
                title="Error",
                description="API Request Fail",
                colour=0xff0000,
                timestamp=datetime.utcnow()
            )
            for key_i in data.keys():
                if key_i != 'message' and key_i != 'error':
                    new_key = key_i
            embed.add_field(name='Error Code', value=str(
                data['error']), inline=True)
            embed.add_field(name='Error Message', value=str(
                data['message']), inline=True)
            if new_key is not None:
                embed.add_field(name=new_key.title(), value=str(
                    data[new_key]), inline=True)
            embed.set_footer(text="given subreddit: "+subreddit)
            await ctx.send(reference=ctx.message, embed=embed)
        else:
            embed = discord.Embed(title=str("/r/"+subreddit),
                                  colour=0xff5700, timestamp=datetime.utcnow())
            embed.set_thumbnail(
                url="https://user-images.githubusercontent.com/63065397/156344382-821872f3-b6e3-46e7-b925-b5f1a0821da8.png")
            i = 1
            if number is None:
                number = 5
            for head in (data['data']['children']):
                embed.add_field(
                    name=str(i),
                    value=head['data']['title'][0:127] + "...",
                    inline=False
                )
                i += 1
                if i > number:
                    break
            if i <= number:
                embed.add_field(
                    name=str(i),
                    value="No more data could be received...",
                    inline=False
                )
            if number > 0:
                await ctx.send(reference=ctx.message, embed=embed)
            return
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_crypto_rate(self, urlEnd):
        # ids=bitcoin&vs_currencies=inr
        API_URL = "https://api.coingecko.com/api/v3/simple/price?" + urlEnd
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                quote_json = await resp.json(content_type=None)
                return (quote_json)

    @commands.command(name="crypto", aliases=["cryptocurrency", "crypto-price", "coingecko"], help="shows the price of given cryptocurrency(s) in given currency(s)")
    async def crypto_command(self, ctx, cryptocurrencies: str, currencies: Optional[str]):
        if currencies is None:
            currencies = "usd"
        cryptocurrencies = cryptocurrencies.lower()
        cryptocurrencies = cryptocurrencies.split(",")
        for i in range(len(cryptocurrencies)):
            cryptocurrencies[i] = cryptocurrencies[i].strip()
        cryptocurrencies = ",".join(cryptocurrencies)
        currencies = currencies.lower()
        currencies = currencies.split(",")
        for i in range(len(currencies)):
            currencies[i] = currencies[i].strip()
        currencies = ",".join(currencies)
        urlEnd = "ids="+cryptocurrencies+"&vs_currencies="+currencies
        rate = await self.get_crypto_rate(urlEnd)
        if (len(rate) == 0) or (len(rate[list(rate.keys())[0]]) == 0):
            async with ctx.typing():
                embed = discord.Embed(
                    title="",
                    description="",
                    color=0xff0000
                )
                embed.set_author(
                    name="Unknown error occured")
            await ctx.send(reference=ctx.message, embed=embed)
            return
        for cryptocurrency in rate.keys():
            async with ctx.typing():
                embed = discord.Embed(
                    title="",
                    description="",
                    color=0x00ff00
                )
                embed.set_author(
                    name=cryptocurrency.title()+" Price")
                for currency in rate[cryptocurrency].keys():
                    embed.add_field(
                        name=currency.upper(),
                        value=("{:,}".format(rate[cryptocurrency][currency])),
                        inline=True
                    )
            await ctx.send(reference=ctx.message, embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="tts", aliases=["text-to-speech"], help="converts given text to speech in given language")
    async def tts_command(self, ctx, req_lang, *, text):
        req_lang = req_lang.lower()
        if req_lang not in [key.lower() for key in lang.tts_langs().keys()]:
            for k, v in lang.tts_langs().items():
                if req_lang in v.lower():
                    req_lang = k.lower()
                    break
                if req_lang == k.lower():
                    req_lang = k
                    break
        if req_lang not in [key.lower() for key in lang.tts_langs().keys()]:
            with ctx.typing():
                closest_match = difflib.get_close_matches(req_lang, [key.lower() for key in lang.tts_langs().keys()] + [val.lower() for val in lang.tts_langs().values()])
                if len(closest_match) > 0:
                    did_you_mean = "\nDid you mean: " + ", ".join(closest_match)
                else:
                    did_you_mean = ""
                embed = discord.Embed(
                    title="Error",
                    description="Language not found" + did_you_mean,
                    colour=0xff0000,
                    timestamp=datetime.utcnow()
                )
            await ctx.send(reference=ctx.message, embed=embed)
            return
        if len(text) > 200:
            embed = discord.Embed(
                title="Error",
                description="Text too long",
                colour=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="given text: "+text)
            await ctx.send(reference=ctx.message, embed=embed)
            return
        if len(text) == 0:
            embed = discord.Embed(
                title="Error",
                description="Nothing to read",
                colour=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="given text: "+text)
            await ctx.send(reference=ctx.message, embed=embed)
            return
        tts = gTTS(text=text, lang=req_lang)
        tts.save("tts.mp3")
        await ctx.send(file=discord.File("tts.mp3"))
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="trivia-cat", aliases=["qna-cat", "qna-categories", "trivia-categories"], help="shows the categories with their IDs of trivia questions")
    async def trivia_cat_command(self, ctx):
        # send self.trivia_categories to ctx in two embeds (max 25 fields per embed)
        for i in range(len(self.trivia_categories)//25 + (len(self.trivia_categories) % 25 != 0)):
            embed = discord.Embed(
                title="Trivia Categories",
                description="",
                colour=0x11ffaa,
                timestamp=datetime.utcnow()
            )
            for j in range(25):
                if i*25+j < len(self.trivia_categories):
                    embed.add_field(
                        name=self.trivia_categories[i*25+j]['title'].title(),
                        value="ID: " + str(i*25+j) + "\nQuestion Count: " + str(self.trivia_categories[i*25+j]['clues_count']),
                        inline=True
                    )
            embed.set_footer(text="Page "+str(i+1)+"/"+str(len(self.trivia_categories)//25 + (len(self.trivia_categories) % 25 != 0)))

            await ctx.send(reference=ctx.message, embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_qa(self, urlEnd):
        API_URL = "https://jservice.io/api/clues?category=" + urlEnd
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                quote_json = await resp.json(content_type=None)
                return (quote_json)

    @commands.command(name="trivia", aliases=["q/a", "ask", "question", "qna"], help="shows a question of given category id and it's answer")
    async def trivia_command(self, ctx, category_id: Optional[int]):
        if category_id is None:
            category_id = randint(0, len(self.trivia_categories)-1)
        if category_id < 0 or category_id >= len(self.trivia_categories):
            embed = discord.Embed(
                title="Error",
                description="category ID out of range",
                colour=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="given category ID: "+str(category_id))
            await ctx.send(reference=ctx.message, embed=embed)
            return
        
        question = await self.get_qa(str(self.trivia_categories[category_id]['id']))
        if len(question) == 0:
            embed = discord.Embed(
                title="Error",
                description="no question found",
                colour=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="given category ID: "+str(category_id))
            await ctx.send(reference=ctx.message, embed=embed)
            return
        ind = randint(0, len(question)-1)
        async with ctx.typing():
            embed = discord.Embed(
                title="Question",
                description=question[ind]['question'],
                color=0x00ff00
            )
            embed.add_field(
                name="Category",
                value="||" + str(question[ind]['category']['title']).title() + "||",
                inline=True
            )
            embed.add_field(
                name="Difficulty",
                value="||" + str(question[ind]['value']) + "||",
                inline=True
            )
            embed.add_field(
                name="Answer",
                value="||" + str(question[ind]['answer']) + "||",
                inline=False
            )
        await ctx.send(reference=ctx.message, embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Fun(bot))
