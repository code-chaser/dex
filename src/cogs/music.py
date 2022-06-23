import discord
import aiohttp
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
                data = data['entries'][0]
        else:
            return None

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)
    # ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class Music(commands.Cog):

    # queue format:
    # query/url(str) | download(bool) | ctx(ctx)
    music_queue = []
    popped = 0
    current = -1
    queued = 0
    loop_queue = False
    repeat_song = False
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

    embed_error_no_vc_dex = discord.Embed(
        title="Error",
        description=''.join(
            "Dex is not in any voice channel\n**Use `<prefix> join` to make it connect to one and then use music commands**"),
        colour=0xff0000,
        timestamp=datetime.datetime.utcnow()
    )

    MUSIC_ICON = "https://user-images.githubusercontent.com/63065397/156855077-ce6e0896-cc81-4d4d-98b8-3e7b70050afe.png"
    # ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.MUSIC_ICON = "https://user-images.githubusercontent.com/63065397/156855077-ce6e0896-cc81-4d4d-98b8-3e7b70050afe.png"
        self.currently_playing_music = ()
        self.currently_playing_player = None
        self.music_queue = []
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="join", aliases=["connect"], help="joins the voice channel of the author")
    async def join_command(self, ctx):
        if ctx.author.voice is None:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=ctx.author.mention + ", you are not connected to a voice channel",
                    colour=0xFF0000,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_footer(text="join request from " + ctx.author.name)
            await ctx.send(embed=embed)
            return False

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
            return True
        else:
            if (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()) and (ctx.voice_client.channel != ctx.author.voice.channel):
                async with ctx.typing():
                    embed = discord.Embed(
                        title="Error",
                        description=''.join(
                            "Can't move b/w channels while playing music!\n**NOTE: **You can still add music to the queue!"),
                        colour=0xff0000,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_footer(
                        text="join request from " + ctx.author.name)
                await ctx.send(embed=embed)
                return True
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                return True
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="leave", aliases=["disconnect, dc"], help="leaves if connected to any voice channel")
    async def leave_command(self, ctx):
        self.music_queue.clear()
        self.currently_playing_music = None
        self.current = -1
        self.popped = 0
        self.queued = 0
        self.loop_queue = False
        self.repeat_song = False
        self.currently_playing_player = None
        if ctx.voice_client is None:
            embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
        else:
            await ctx.voice_client.disconnect()
    # ----------------------------------------------------------------------------------------------------------------------

    async def play_music_from_player(self, ctx, *, player):
        if player is None:
            return
        self.currently_playing_player = player
        embed = discord.Embed(
            title="Now Playing",
            description="- requested by " +
            self.music_queue[self.current][1].author.mention,
            colour=0x00ff00,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=self.MUSIC_ICON)
        embed.set_author(name=player.title, url=player.url,
                         icon_url=ctx.author.avatar_url)
        embed.add_field(name="Title", value=player.title, inline=False)
        embed.add_field(name="Position in queue",
                        value=self.current+1, inline=False)
        ctx.voice_client.play(player, after=lambda e: print(
            f'Player error: {e}') if e else None)
        await ctx.send(embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------

    async def keep_playing(self, ctx):
        while ((len(self.music_queue) - self.current > 1) or (self.loop_queue is True)) and (len(self.music_queue) > 0):
            if ((not ctx.voice_client.is_playing()) and (not ctx.voice_client.is_paused())):
                self.is_playing = True
                if (not self.repeat_song) or (self.current == -1):
                    self.current += 1
                if self.popped == len(self.music_queue):
                    self.popped = 0
                if self.current == len(self.music_queue):
                    self.current = 0
                player = await YTDLSource.from_url(self.music_queue[self.current][2], loop=self.bot.loop, stream=self.music_queue[self.current][3])
                self.music_queue[self.current][0] = player
                await self.play_music_from_player(self.music_queue[self.current][1], player=player)
                if not self.repeat_song:
                    self.popped += 1
            await asyncio.sleep(0.5)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="play", aliases=["stream", "p", "add"], help="streams a song directly from youtube")
    async def play_command(self, ctx, *, url: typing.Optional[str]):
        if (url is None) and (ctx.message.content[(len(ctx.message.content)-3):(len(ctx.message.content))] != "add"):
            if ctx.voice_client is None:
                await self.join_command(ctx)
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
            async with ctx.typing():
                embed = discord.Embed(
                    title="Status",
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
                n = "Error"
                v = "Missing required arguements"
                embed.add_field(name=n, value=v, inline=False)
            await ctx.send(embed=embed)
            return

        joined = await self.join_command(ctx)
        if joined == False:
            return
        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        if player is None:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(self.bad_request_error_message),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow(),
                )
            await ctx.send(embed=embed)
            return
        self.music_queue.append([player, ctx, url, True])
        self.queued += 1
        async with ctx.typing():
            embed = discord.Embed(
                title="Added to queue",
                description="\"" + url + "\" requested by " + ctx.author.mention,
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name=player.title, url=player.url,
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline=False)
            embed.add_field(name="Queue Position", value=len(
                self.music_queue), inline=True)
        await ctx.send(embed=embed)
        await self.keep_playing(ctx)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="playm", aliases=["streamm", "pm", "addm"], help="plays multiple songs (seperated by semicolons ';')")
    async def playm_command(self, ctx, *, args):
        urls = args.split(';')
        joined = await self.join_command(ctx)
        if joined == False:
            return
        for url in urls:
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            if player is None:
                async with ctx.typing():
                    embed = discord.Embed(
                        title="Error",
                        description=''.join(self.bad_request_error_message),
                        colour=0xff0000,
                        timestamp=datetime.datetime.utcnow(),
                    )
                await ctx.send(embed=embed)
                continue
            self.music_queue.append([player, ctx, url, True])
            self.queued += 1
            async with ctx.typing():
                embed = discord.Embed(
                    title="Added to queue",
                    description="\"" + url + "\" requested by " + ctx.author.mention,
                    colour=0x00ff00,
                    timestamp=datetime.datetime.utcnow(),
                )
                embed.set_thumbnail(url=self.MUSIC_ICON)
                embed.set_author(name=player.title, url=player.url,
                                 icon_url=ctx.author.avatar_url)
                embed.add_field(name="Title", value=player.title, inline=False)
                embed.add_field(name="Queue Position", value=len(
                    self.music_queue), inline=True)
            await ctx.send(embed=embed)
        await self.keep_playing(ctx)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name='dplay', help="downloads a song and then queues it to reduce any possible lags")
    async def dplay_command(self, ctx, *, url):
        joined = await self.join_command(ctx)
        if joined == False:
            return
        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        if player is None:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(self.bad_request_error_message),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        self.music_queue.append([player, ctx, url, False])
        self.queued += 1
        async with ctx.typing():
            embed = discord.Embed(
                title="Downloaded & Added to queue",
                description="\"" + url + "\" requested by " + ctx.author.mention,
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name=player.title, url=player.url,
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline=False)
            embed.add_field(name="Queue Position", value=len(
                self.music_queue), inline=True)
        await ctx.send(embed=embed)
        await self.keep_playing(ctx)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name='dplaym', help="dplays multiple songs (seperated by semicolons ';')")
    async def dplaym_command(self, ctx, *, args):
        urls = args.split(';')
        joined = await self.join_command(ctx)
        if joined == False:
            return
        for url in urls:
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            if player is None:
                async with ctx.typing():
                    embed = discord.Embed(
                        title="Error",
                        description=''.join(self.bad_request_error_message),
                        colour=0xff0000,
                        timestamp=datetime.datetime.utcnow()
                    )
                await ctx.send(embed=embed)
                continue
            self.music_queue.append([player, ctx, url, False])
            self.queued += 1
            async with ctx.typing():
                embed = discord.Embed(
                    title="Downloaded & Added to queue",
                    description="\"" + url + "\" requested by " + ctx.author.mention,
                    colour=0x00ff00,
                    timestamp=datetime.datetime.utcnow(),
                )
                embed.set_thumbnail(url=self.MUSIC_ICON)
                embed.set_author(name=player.title, url=player.url,
                                 icon_url=ctx.author.avatar_url)
                embed.add_field(name="Title", value=player.title, inline=False)
                embed.add_field(name="Queue Position", value=len(
                    self.music_queue), inline=True)
            await ctx.send(embed=embed)
        await self.keep_playing(ctx)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name='loop', help="toggles looping of the queue")
    async def loop_command(self, ctx, loop_switch: typing.Optional[str]):

        if ctx.voice_client is None:
            async with ctx.typing():
                embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
            return

        if loop_switch is None:
            self.loop_queue = not self.loop_queue
            if self.loop_queue:
                loop_switch = "on"
            else:
                loop_switch = "off"
        elif loop_switch.lower() == "on":
            self.loop_queue = True
        elif loop_switch.lower() == "off":
            self.loop_queue = False
        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Status",
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.add_field(
                    name="Error",
                    value="Invalid value provided",
                    inline=True
                )
            await ctx.send(embed=embed)
            return
        async with ctx.typing():
            embed = discord.Embed(
                title="Status",
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(
                name="Done",
                value="Queue looping is now " + loop_switch.lower(),
                inline=True
            )
        await ctx.send(embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name='repeat', help="toggles repeating of the currently playing song")
    async def repeat_command(self, ctx, repeat_switch: typing.Optional[str]):

        if ctx.voice_client is None:
            async with ctx.typing():
                embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
            return

        if repeat_switch is None:
            self.repeat_song = not self.repeat_song
            if self.repeat_song:
                repeat_switch = "on"
            else:
                repeat_switch = "off"
        elif repeat_switch.lower() == "on":
            self.repeat_song = True
        elif repeat_switch.lower() == "off":
            self.repeat_song = False
        else:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Status",
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
                embed.add_field(
                    name="Error",
                    value="Invalid value provided",
                    inline=True
                )
            await ctx.send(embed=embed)
            return
        async with ctx.typing():
            embed = discord.Embed(
                title="Status",
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            embed.add_field(
                name="Done",
                value="Song repeat is now " + repeat_switch.lower(),
                inline=True
            )
        await ctx.send(embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="queue", aliases=["view"], help="displays the current queue")
    async def queue_command(self, ctx, *, url: typing.Optional[str]):
        if url is not None:
            if url != "":
                await self.play_command(ctx, url=url)
                return

        if ctx.voice_client is None:
            async with ctx.typing():
                embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
            return

        if len(self.music_queue) == 0:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Queue",
                    description=''.join(
                        "Queue is empty, nothing to play\nUse `<prefix> play <query/url>` to add to queue"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(
            title="Queue",
            colour=0x0000ff,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=self.MUSIC_ICON)
        embed.set_author(name="Dex", icon_url=self.bot.user.avatar_url)
        size = len(self.music_queue)
        for i in range(0, size, 25):
            for j in range(i, min(size, i + 25)):
                k = "**" if j == self.current else ""
                embed.add_field(
                    name=str(j + 1) + (" ***(Currently Playing)***" if j == self.current else ""), value=k+str(self.music_queue[j][0].title)+k, inline=False)
            async with ctx.typing():
                embed.set_footer(
                    text="Page " + str(int(i / 25) + 1) + " of " + str(int(size / 25) + 1))
            await ctx.send(embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="remove", help="removes a song from the queue, takes song position as argument")
    async def remove_command(self, ctx, pos):
        if ctx.voice_client is None:
            async with ctx.typing():
                embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
            return
        if (pos is None):
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(
                        "Missing required argument: `<position>`"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        if (1 > int(pos)) or (len(self.music_queue) < int(pos)):
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=str(
                        "Queue Position must be between (1 & "+str(len(self.music_queue))+")"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        pos = int(pos) - 1
        async with ctx.typing():
            embed = discord.Embed(
                title="Removed from queue",
                description="track requested by " +
                self.music_queue[int(pos)][1].author.mention,
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            player = self.music_queue[int(pos)][0]
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name=player.title, url=player.url,
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline=False)
            embed.add_field(name="Remove request by",
                            value=ctx.author.mention, inline=True)
        self.music_queue.pop(int(pos))
        if self.current > pos:
            self.current -= 1
            self.popped -= 1
        elif self.current == pos:
            self.repeat_song = False
            self.current -= 1
            ctx.voice_client.stop()
        await ctx.send(embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="jump", alises=["jumpto"], help="jumps to a song in the queue, takes song position as argument")
    async def jump_command(self, ctx, pos):
        pos = int(pos)
        if ctx.voice_client is None:
            async with ctx.typing():
                embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
            return
        if (pos is None):
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=''.join(
                        "Missing required argument: `<position>`"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        if (1 > int(pos)) or (len(self.music_queue) < int(pos)):
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description=str(
                        "Queue Position must be between (1 & "+str(len(self.music_queue))+")"),
                    colour=0xff0000,
                    timestamp=datetime.datetime.utcnow()
                )
            await ctx.send(embed=embed)
            return
        pos = int(pos) - 1
        async with ctx.typing():
            embed = discord.Embed(
                title="Jumping to " + str(pos + 1),
                description="- requested by " + ctx.author.mention,
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            player = self.music_queue[int(pos)][0]
            embed.set_thumbnail(url=self.MUSIC_ICON)
            embed.set_author(name=player.title, url=player.url,
                             icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline=False)
            embed.add_field(
                name="Queue Looping", value="On" if self.loop_queue else "Off", inline=True)
        await ctx.send(embed=embed)
        self.repeat_song = False
        self.popped = pos
        self.current = pos - 1
        ctx.voice_client.stop()
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="volume", aliases=["vol"], help="changes the volume of the music player")
    async def volume_command(self, ctx, volume: int):
        if ctx.voice_client is None:
            async with ctx.typing():
                embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
            return
        ctx.voice_client.source.volume = volume / 100
        async with ctx.typing():
            embed = discord.Embed(
                title=str(volume) + "%",
                colour=0x00ff00,
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name="Volume set to",
                             icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="stop", aliases=["stfu", "shut"], help="stops the music player and clears the queue")
    async def stop_command(self, ctx):
        self.current = -1
        self.popped = 0
        self.queued = 0
        self.loop_queue = False
        self.repeat_song = False
        self.currently_playing_music = None
        self.currently_playing_player = None
        if ctx.voice_client is None:
            async with ctx.typing():
                embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
            return
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            self.music_queue.clear()
            ctx.voice_client.stop()
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="pause", help="pauses the music player")
    async def pause_command(self, ctx):
        if ctx.voice_client is None:
            embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
        elif ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="resume", help="resumes the music player")
    async def resume_command(self, ctx):
        if ctx.voice_client is None:
            embed = self.embed_error_no_vc_dex
            await ctx.send(embed=embed)
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        elif len(self.music_queue) > 0:
            if not ctx.voice_client.is_playing():
                await self.keep_playing(ctx)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="skip", aliases=["next"], help="skips the currently playing song")
    async def skip_command(self, ctx):
        if ctx.voice_client is None:
            async with ctx.typing():
                embed = self.embed_error_no_vc_dex
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
                self.repeat_song = False
                self.popped += 1
                ctx.voice_client.stop()
        return
    # ----------------------------------------------------------------------------------------------------------------------

    async def get_lyrics(self, song_title):
        API_URL = "https://some-random-api.ml/lyrics?title=" + song_title
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as response:
                data_json = await response.json()
                return data_json
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name='lyrics', help='sends the lyrics of the song')
    async def lyrics_command(self, ctx, *args) -> None:
        song_title = ''
        for arg in args:
            song_title += arg+'%20'
        if len(song_title) > 0:
            song_title = song_title[:-3]
        else:
            if self.currently_playing_player is None:
                async with ctx.typing():
                    embed = discord.Embed(
                        title="Error",
                        description="No song is currently playing",
                        color=0xff0000,
                        timestamp=datetime.datetime.utcnow(),
                    )
                await ctx.send(embed=embed)
                return
            args = self.currently_playing_player.title.split()
            for arg in args:
                song_title += arg+'%20'
            song_title = song_title[:-3]

        data = await self.get_lyrics(song_title)
        if not 'lyrics' in data.keys():
            err_mssg = data['error']
            embed = discord.Embed(
                title="Error",
                description=err_mssg +
                ('\n'+'[see results from GoogleSearch](https://www.google.com/search?q='+song_title+'+lyrics)'),
                colour=0xff0000,
                timestamp=datetime.datetime.utcnow(),
            )
            await ctx.send(embed=embed)
        else:
            async with ctx.typing():
                lyrics = data['lyrics']
                extend_text = '\n[see results from GoogleSearch](https://www.google.com/search?q=' + \
                    song_title+'+lyrics)'
                if len(lyrics) > 3500:
                    lyrics = lyrics[:3500]+'... '
                    extend_text = '[read more](https://www.google.com/search?q=' + \
                        song_title+'+lyrics)'

                embed = discord.Embed(
                    title=data['title'],
                    description=lyrics+extend_text,
                    color=0x00ff00,
                    timestamp=datetime.datetime.utcnow(),
                )
                embed.set_author(
                    name=data['author'],
                )
                embed.set_thumbnail(url=data['thumbnail']['genius'])
                embed.set_footer(
                    icon_url=ctx.author.avatar_url,
                )
            await ctx.send(embed=embed)
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Music(bot))
