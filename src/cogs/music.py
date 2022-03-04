import discord
import youtube_dl
import asyncio
from typing import Optional
from datetime import datetime
from discord import Embed, Member, Guild
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
    'source_address': '0.0.0.0' # binds to ipv4 since ipv6 addresses cause issues sometimes
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

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)


class Music(commands.Cog):
    
    # queue format:
    # query/url(str) | download(bool) | ctx(ctx)
    music_queue = []
    is_playing = False
    
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue = []

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
                return
            else:
                embed=Embed(
                    title="Error",
                    description=ctx.author.mention + ", you are not connected to a voice channel",
                    colour = 0xFF0000,
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text="join request from " + ctx.author.name)
                await ctx.send(embed=embed)
                return
        else:
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                pass
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
                return
        embed = Embed(
            title="Error",
            description=''.join("Can't move b/w channels while playing music!\n**NOTE: **You can still add music to the queue!"),
            colour = 0xff0000,
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="join request from " + ctx.author.name)
        await ctx.send(embed=embed)
        
    
    async def make_join(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                embed=Embed(
                    title="Error",
                    description=ctx.author.mention + ", you are not connected to a voice channel",
                    colour = 0xFF0000,
                    timestamp=datetime.utcnow()
                )
                await ctx.send(embed=embed)
                return
        else:
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                pass
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)

    async def download_play(self, ctx, *, url):
        """Downloads and plays, from a url (almost anything youtube_dl supports)"""
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            embed = Embed(
                title = "Downloading",
                description = str(player.url),
                colour = 0x0000ff,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Title", value=player.title, inline = False)
            embed.add_field(name="Duration", value=player.duration, inline = True)
            embed.add_field(name="Requested by", value=ctx.author.mention, inline = True)
            
        await ctx.send(embed=embed)
        
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            embed = Embed(
                title = "Now Playing",
                description = str(player.url),
                colour = 0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Title", value=player.title, inline = False)
            embed.add_field(name="Duration", value=player.duration, inline = True)
            embed.add_field(name="Requested by", value=ctx.author.mention, inline = True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(embed=embed)
        
    async def stream_play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            embed = Embed(
                title = "Now Playing",
                description = str(player.url),
                colour = 0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=player.thumbnail)
            embed.set_author(name=player.title, url=player.url, icon_url="https://user-images.githubusercontent.com/63065397/156735015-d12baec8-3ea9-4d23-a577-ebdcb3909566.png")
            embed.add_field(name="Title", value=player.title, inline = False)
            embed.add_field(name="Duration", value=player.duration, inline = False)
            embed.add_field(name="Requested by", value=ctx.author.mention, inline = False)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(embed=embed)
    
    async def keep_playing(self, ctx):
        while len(self.music_queue) > 0:
            if not ctx.voice_client.is_playing():
                self.is_playing = True
                if self.music_queue[0][1]:
                    await self.download_play(self.music_queue[0][2], url=self.music_queue[0][0])
                else:
                    await self.stream_play(self.music_queue[0][2], url=self.music_queue[0][0])
                self.music_queue.pop(0)
            await asyncio.sleep(1)

        self.is_playing = False
        
    
    @commands.command(name="play", aliases=["stream"],help = "streams a song directly from youtube")
    async def add_to_queue_0(self, ctx, *, url: Optional[str]):
        if url is None:
            await ctx.voice_client.resume()
        async with ctx.typing():
            await self.make_join(ctx)
            if ctx.voice_client is None:
                return
            self.music_queue.append([url, False, ctx])
            embed = Embed(
                title="Added to queue",
                description=url + " requested by " + ctx.author.mention,
                colour = 0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156735015-d12baec8-3ea9-4d23-a577-ebdcb3909566.png")
            embed.add_field(name="Queue Position", value=len(self.music_queue), inline = True)
            await ctx.send(embed=embed)
            
        if not ctx.voice_client.is_playing():
            await self.keep_playing(ctx)
    
    @commands.command(name = 'dplay', help="downloads a song and then plays it to reduce any possible lags")
    async def add_to_queue_1(self, ctx, *, url):
        async with ctx.typing():
            await self.make_join(ctx)
            self.music_queue.append([url, True, ctx])
            embed = Embed(
                title="Added to queue",
                description=url + " requested by " + ctx.author.mention,
                colour = 0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156735015-d12baec8-3ea9-4d23-a577-ebdcb3909566.png")
            embed.add_field(name="Queue Position", value=len(self.music_queue), inline = True)
            await ctx.send(embed=embed)
            
        if not ctx.voice_client.is_playing():
            await self.keep_playing(ctx)
    

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        self.music_queue.clear()
        await ctx.voice_client.stop()
    
    @commands.command(name="pause")
    async def pause(self,ctx):
        await ctx.voice_client.pause()
    
    @commands.command(name="resume")
    async def resume(self,ctx):
        await ctx.voice_client.resume()

    @commands.command(name="leave", aliases=["disconnect"], help="leaves if connected to any vc")
    async def leave_vc(self, ctx):
        self.music_queue.clear()
        if ctx.voice_client is None:
            embed=Embed(
                title="Error",
                description="Dex is not in any voice channel",
                colour=0xff0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            await ctx.guild.voice_client.disconnect()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')
        

def setup(bot):
    bot.add_cog(Music(bot))