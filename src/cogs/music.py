import discord
import requests
import json
import youtube_dl
import asyncio
import typing
import datetime
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


YTDL_FORMAT_OPTIONS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # binds to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(YTDL_FORMAT_OPTIONS)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if data is not None:
            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]
        else:
            return None

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)


class Music(commands.Cog):

    # queue format:
    # query/url(str) | download(bool) | ctx(ctx)
    music_queue = []
    currently_playing_music = ()
    currently_playing_player = None
    is_playing = False

    bad_request_error_message = ''
    bad_request_error_message += (
        ''.join("Bad response while searching for the music\n\n"))
    bad_request_error_message += (''.join("**Possible causes include:**\n"))
    bad_request_error_message += (
        ''.join("*1. bad network on the bot's end;\n"))
    bad_request_error_message += (
        ''.join("2. the given search query couldn't find matching results;*\n"))
    bad_request_error_message += (''.join(
        "***3. too many queuing requests made, without letting the bot to respond to them;***\n"))
    bad_request_error_message += (''.join(
        "\n**To avoid any further unexpected errors, make the bot rejoin the voice channel using `<prefix> leave` and then `<prefix> join`**\n"))
    bad_request_error_message += (''.join("**SORRY FOR THE INCONVENIENCE!**"))

    MUSIC_ICON = "https://user-images.githubusercontent.com/63065397/156855077-ce6e0896-cc81-4d4d-98b8-3e7b70050afe.png"

    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.MUSIC_ICON = "https://user-images.githubusercontent.com/63065397/156855077-ce6e0896-cc81-4d4d-98b8-3e7b70050afe.png"
        self.currently_playing_music = ()
        self.currently_playing_player = None
        self.music_queue = []

    @commands.command(name="join", aliases=["connect"], help="joins the voice channel of the author")
    async def join_vc(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice is not None:
                await ctx.author.voice.channel.connect()
                return
            else:
                embed = discord.Embed(
                    title="Error",
                    description=ctx.author.mention + ", you are not connected to a voice channel",
                    colour=0xFF0000,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_footer(text="join request from " + ctx.author.name)
                await ctx.send(embed=embed)
                return
        else:
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                pass
            else:
                if ctx.author.voice is not None:
                    await ctx.voice_client.move_to(ctx.author.voice.channel)
                    return
                else:
                    embed = discord.Embed(
                        title="Error",
                        description=ctx.author.mention + ", you are not connected to a voice channel",
                        colour=0xFF0000,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_footer(
                        text="join request from " + ctx.author.name)
                    await ctx.send(embed=embed)
                    return
        embed = discord.Embed(
            title="Error",
            description=''.join(
                "Can't move b/w channels while playing music!\n**NOTE: **You can still add music to the queue!"),
            colour=0xff0000,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="join request from " + ctx.author.name)
        await ctx.send(embed=embed)

    async def make_join(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(
                    title="Error",
                    description=ctx.author.mention + ", you are not connected to a voice channel",
                    colour=0xFF0000,
                    timestamp=datetime.datetime.utcnow()
                )
                await ctx.send(embed=embed)
                return
        else:
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                pass
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)

    async def play_music_from_player(self, ctx, *, player):
        if player is None:
            return
        self.currently_playing_player = player
        embed = discord.Embed(
            title="Now Playing",
            description="- requested by " +
            self.music_queue[0][1].author.mention,
            colour=0x00ff00,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=self.MUSIC_ICON)
        embed.set_author(name=player.title, url=player.url,
                         icon_url=ctx.author.avatar_url)
        embed.add_field(name="Title", value=player.title, inline=False)
        embed.add_field(name="Remaining in queue",
                        value=len(self.music_queue)-1, inline=False)
        ctx.voice_client.play(player, after=lambda e: print(
            f'Player error: {e}') if e else None)
        await ctx.send(embed=embed)

    _random_int = 0

    async def keep_playing(self, ctx):
        while len(self.music_queue) > 0:
            if (not ctx.voice_client.is_playing()) and (not ctx.voice_client.is_paused()):
                self.is_playing = True
                await self.play_music_from_player(self.music_queue[0][1], player=self.music_queue[0][0])
                self.music_queue.pop(0)
            await asyncio.sleep(0.5)

    @commands.command(name="play", aliases=["stream", "p", "add"], help="streams a song directly from youtube")
    async def add_to_queue_0(self, ctx, *, url: typing.Optional[str]):
        if (url is None) and (ctx.message.content[(len(ctx.message.content)-3):(len(ctx.message.content))] != "add"):
            if ctx.voice_client is None:
                await self.make_join(ctx)
            if ctx.voice_client is None:
                return
            if ctx.voice_client.is_playing():
                return
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
            elif len(self.music_queue) > 0:
                if not ctx.voice_client.is_playing():
                    await self.keep_playing(ctx)
            else:
                embed = discord.Embed(
                    title="Error",
                    description=''.join(
                        "Queue is empty, nothing to play\nUse `<prefix> play <query/url>` to add to queue"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
                await ctx.send(embed=embed)
            return
        elif url is None:
            embed = discord.Embed(
                title="Status",
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow()
            )
            n = "Error"
            v = "Missing required arguements"
            embed.add_field(name=n, value=v, inline=False)
            await ctx.send(embed=embed)

        async with ctx.typing():
            await self.make_join(ctx)
            if ctx.voice_client is None:
                return
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            if player is None:
                with ctx.typing():
                    embed = discord.Embed(
                        title="Error",
                        description=''.join(self.bad_request_error_message),
                        colour=0xff0000,
                        timestamp=datetime.datetime.utcnow()
                    )
                await ctx.send(embed=embed)
                return
            self.music_queue.append([player, ctx])
            embed = discord.Embed(
                title="Added to queue",
                description="\"" + url + "\" requested by " + ctx.author.mention,
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name=player.title, url=player.url,
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline=False)
            embed.add_field(name="Queue Position", value=len(
                self.music_queue), inline=True)
        await ctx.send(embed=embed)
        await self.keep_playing(ctx)

    @commands.command(name='dplay', help="downloads a song and then plays it to reduce any possible lags")
    async def add_to_queue_1(self, ctx, *, url):
        async with ctx.typing():
            await self.make_join(ctx)
            if ctx.voice_client is None:
                return
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            if player is None:
                with ctx.typing():
                    embed = discord.Embed(
                        title="Error",
                        description=''.join(self.bad_request_error_message),
                        colour=0xff0000,
                        timestamp=datetime.datetime.utcnow()
                    )
                await ctx.send(embed=embed)
                return
            self.music_queue.append([player, ctx])
            embed = discord.Embed(
                title="Downloaded & Added to queue",
                description="\"" + url + "\" requested by " + ctx.author.mention,
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name=player.title, url=player.url,
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline=False)
            embed.add_field(name="Queue Position", value=len(
                self.music_queue), inline=True)
        await ctx.send(embed=embed)
        await self.keep_playing(ctx)

    # @commands.command(name="loop", help="loops the currently playing song")
    # async def loop(self, ctx):
    #     if ctx.voice_client is None:
    #         with ctx.typing():
    #             embed=discord.Embed(
    #                 title="Error",
    #                 description=''.join("Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one and then use music commands**"),
    #                 colour=0xff0000,
    #                 timestamp=datetime.datetime.utcnow()
    #             )
    #         await ctx.send(embed=embed)
    #         return
    #     if (not ctx.voice_client.is_playing()) and (not ctx.voice_client.is_paused()):
    #         with ctx.typing():
    #             embed=discord.Embed(
    #                 title="Error",
    #                 description=''.join("Queue is empty, nothing to loop through\nUse `<prefix> play <query/url>` to add to queue"),
    #                 colour=0xff0000,
    #                 timestamp=datetime.datetime.utcnow()
    #             )
    #         await ctx.send(embed=embed)
    #         return
    #     while True:

    @commands.command(name="queue", aliases=["view"], help="displays the current queue")
    async def view_queue(self, ctx, *args):
        if (ctx.message.content[(len(ctx.message.content)-5):(len(ctx.message.content))] == "queue"):
            url = "".join(args)
            if url != "":
                await self.add_to_queue_0(ctx, url)
                return
        if ctx.voice_client is None:
            with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(
                        "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one and then use music commands**"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        if len(self.music_queue) == 0:
            with ctx.typing():
                embed = discord.Embed(
                    title="Queue",
                    description=''.join(
                        "Queue is empty, nothing to play\nUse `<prefix> play <query/url>` to add to queue"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        with ctx.typing():
            embed = discord.Embed(
                title="Queue",
                colour=0x0000ff,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name="Dex", icon_url=self.bot.user.avatar_url)
            size = len(self.music_queue)
            for i in range(0, size, 25):
                if i + 25 > size:
                    for j in range(i, size):
                        embed.add_field(
                            name=str(j + 1), value=self.music_queue[j][0].title, inline=False)
                else:
                    for j in range(i, i + 25):
                        embed.add_field(
                            name=str(j + 1), value=self.music_queue[j][0].title, inline=False)
                embed.set_footer(
                    text="Page " + str(int(i / 25) + 1) + " of " + str(int(size / 25) + 1))
                await ctx.send(embed=embed)

    @commands.command(name="remove", help="removes a song from the queue, takes song position as argument")
    async def remove_from_queue(self, ctx, pos):
        pos = int(pos)
        if ctx.voice_client is None:
            with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(
                        "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one and then use music commands**"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        if len(self.music_queue) < int(pos):
            with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join("There are only " + str(len(self.music_queue)) +
                                        " songs in the queue\nNo song at position "+str(pos)+"\n**Use `<prefix> queue` to view the queue**"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        with ctx.typing():
            embed = discord.Embed(
                title="Removed from queue",
                description="track requested by " +
                self.music_queue[int(pos)-1][1].author.mention,
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            player = self.music_queue[int(pos)-1][0]
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name=player.title, url=player.url,
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline=False)
            embed.add_field(name="Remove request by",
                            value=ctx.author.mention, inline=True)
        self.music_queue.pop(int(pos)-1)
        await ctx.send(embed=embed)

    @commands.command(name="jump", help="jumps to a song in the queue, takes song position as argument")
    async def jump_to(self, ctx, pos):
        pos = int(pos)
        if ctx.voice_client is None:
            with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(
                        "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one and then use music commands**"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        if len(self.music_queue) < int(pos):
            with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join("There are only " + str(len(self.music_queue)) +
                                        " songs in the queue\nNo song at position "+str(pos)+"\n**Use `<prefix> queue` to view the queue**"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        with ctx.typing():
            embed = discord.Embed(
                title="Jumping to " + str(pos),
                description="- requested by " + ctx.author.mention,
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            player = self.music_queue[int(pos)-1][0]
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name=player.title, url=player.url,
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline=False)
            embed.add_field(name="Remaining in queue", value=str(
                len(self.music_queue)), inline=True)
        await ctx.send(embed=embed)
        counter = 0
        while counter < int(pos) - 1:
            self.music_queue.pop(0)
            counter += 1
        await self.skip_song(ctx)

    @commands.command(name="volume", aliases=["vol"], help="changes the volume of the music player")
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(
                        "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one and then use music commands**"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        ctx.voice_client.source.volume = volume / 100
        with ctx.typing():
            embed = discord.Embed(
                title=str(volume) + "%",
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name="Volume set to",
                             icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="stop", aliases=["stfu", "shut"], help="stops the music player and clears the queue")
    async def stop_music(self, ctx):
        if ctx.voice_client is None:
            with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(
                        "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one and then use music commands**"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            self.music_queue.clear()
            ctx.voice_client.stop()
        return

    @commands.command(name="pause", help="pauses the music player")
    async def pause(self, ctx):
        if ctx.voice_client is None:
            embed = discord.Embed(
                title="Error",
                description=''.join(
                    "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one**"),
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
        elif ctx.voice_client.is_playing():
            ctx.voice_client.pause()

    @commands.command(name="resume", help="resumes the music player")
    async def resume(self, ctx):
        if ctx.voice_client is None:
            embed = discord.Embed(
                title="Error",
                description=''.join(
                    "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one**"),
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        elif len(self.music_queue) > 0:
            if not ctx.voice_client.is_playing():
                await self.keep_playing(ctx)

    @commands.command(name="leave", aliases=["disconnect, dc"], help="leaves if connected to any voice channel")
    async def leave_vc(self, ctx):
        self.music_queue.clear()
        if ctx.voice_client is None:
            embed = discord.Embed(
                title="Error",
                description=''.join(
                    "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one**"),
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            await ctx.voice_client.disconnect()

    @commands.command(name="skip", aliases=["next"], help="skips the currently playing song")
    async def skip_song(self, ctx):
        if ctx.voice_client is None:
            embed = discord.Embed(
                title="Error",
                description=''.join(
                    "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one**"),
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                async with ctx.typing():
                    embed = discord.Embed(
                        title="Skipping",
                        colour=0x00ff00,
                        timestamp=datetime.datetime.utcnow()
                    )
                    player = self.currently_playing_player
                    embed.set_thumbnail(url=self.MUSIC_ICON)
                    embed.set_author(
                        name=player.title, url=player.url, icon_url=ctx.author.avatar_url)
                    embed.add_field(
                        name="Title", value=player.title, inline=False)
                    embed.add_field(name="Requested by",
                                    value=ctx.author.mention, inline=False)
                    embed.set_footer(text="skip requested by "+ctx.author.name)
                await ctx.send(embed=embed)
                ctx.voice_client.stop()

    @commands.command(name="ping", aliases=["latency"], help="shows the latency of the bot")
    async def ping(self, ctx):
        with ctx.typing():
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
                timestamp=datetime.datetime.utcnow()
            )
        await ctx.send(embed=embed)
    
    def get_lyrics(self, song_title):
        LYRICS_API_URL = "https://some-random-api.ml/lyrics?title="
        response = requests.get(LYRICS_API_URL + song_title)
        response_json = json.loads(response.text)
        return response_json
    
    @commands.command(name="lyrics", help="sends the lyrics of the song")
    async def lyrics_command(self, ctx, *args) -> None:
        song_title=''
        for arg in args:
            song_title+=arg+'%20'
        if len(song_title)>0:
            song_title=song_title[:-3]
        else:
            song_title=self.currently_playing_player.title
        data = self.get_lyrics(song_title)
        if len()


def setup(bot):
    bot.add_cog(Music(bot))
