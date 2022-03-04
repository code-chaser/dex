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
    
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.currently_playing_music = ()
        self.currently_playing_player = None
        self.music_queue = []

    @commands.command(name="join", aliases=["connect"])
    async def join_vc(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice is not None:
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
                if ctx.author.voice is not None:
                    await ctx.voice_client.move_to(ctx.author.voice.channel)
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
        
    async def play_music_from_player(self, ctx, *, player):
        self.currently_playing_player = player
        embed = Embed(
            title = "Now Playing",
            colour = 0x00ff00,
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156735015-d12baec8-3ea9-4d23-a577-ebdcb3909566.png")
        embed.set_author(name=player.title, url=player.url, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Title", value=player.title, inline = False)
        embed.add_field(name="Requested by", value=ctx.author.mention, inline = False)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
        await ctx.send(embed=embed)
    
    async def keep_playing(self, ctx):
        while len(self.music_queue) > 0:
            if (not ctx.voice_client.is_playing()) and (not ctx.voice_client.is_paused()):
                self.is_playing = True
                await self.play_music_from_player(self.music_queue[0][1], player=self.music_queue[0][0])
                self.music_queue.pop(0)
            await asyncio.sleep(0.5)
    
    @commands.command(name="play", aliases=["stream"],help = "streams a song directly from youtube")
    async def add_to_queue_0(self, ctx, *, url: Optional[str]):
        if url is None:
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
                embed=Embed(
                    title="Error",
                    description=''.join("Queue is empty, nothing to play\nUse `<prefix> play <query/url>` to add to queue"),
                    colour = 0xff0000,
                    timestamp=datetime.utcnow()
                )
                await ctx.send(embed=embed)
            return
        async with ctx.typing():
            await self.make_join(ctx)
            if ctx.voice_client is None:
                return
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            self.music_queue.append([player, ctx])
            embed = Embed(
                title = "Added to queue",
                description="\"" + url + "\" requested by " + ctx.author.mention,
                colour = 0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156735015-d12baec8-3ea9-4d23-a577-ebdcb3909566.png")
            embed.set_author(name=player.title, url=player.url, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline = False)
            embed.add_field(name="Queue Position", value=len(self.music_queue), inline = True)
        await ctx.send(embed=embed)
            
        if (not ctx.voice_client.is_playing()) and (not ctx.voice_client.is_paused()):
            await self.keep_playing(ctx)
    
    @commands.command(name = 'dplay', help="downloads a song and then plays it to reduce any possible lags")
    async def add_to_queue_1(self, ctx, *, url):
        async with ctx.typing():
            await self.make_join(ctx)
            if ctx.voice_client is None:
                return
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            self.music_queue.append([player, ctx])
            embed = Embed(
                title = "Downloaded & Added to queue",
                description="\"" + url + "\" requested by " + ctx.author.mention,
                colour = 0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156735015-d12baec8-3ea9-4d23-a577-ebdcb3909566.png")
            embed.set_author(name=player.title, url=player.url, icon_url=ctx.author.avatar_url)
            embed.add_field(name="Title", value=player.title, inline = False)
            embed.add_field(name="Queue Position", value=len(self.music_queue), inline = True)
        await ctx.send(embed=embed)
            
        if (not ctx.voice_client.is_playing()) and (not ctx.voice_client.is_paused()):
            await self.keep_playing(ctx)
    

    @commands.command(name="volume", aliases=["vol"], help="changes the volume of the music player")
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command(name="stop", aliases=["stfu","shut"])
    async def stop_music(self, ctx):
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            self.music_queue.clear()
            ctx.voice_client.stop()
        return
    
    @commands.command(name="pause")
    async def pause(self,ctx):
        if ctx.voice_client is None:
            embed=Embed(
                title="Error",
                description="Dex is not in any voice channel",
                colour=0xff0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif ctx.voice_client.is_playing():
            ctx.voice_client.pause()
    
    @commands.command(name="resume")
    async def resume(self,ctx):
        if ctx.voice_client is None:
            embed=Embed(
                title="Error",
                description="Dex is not in any voice channel",
                colour=0xff0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        elif len(self.music_queue) > 0:
            if not ctx.voice_client.is_playing():
                await self.keep_playing(ctx)

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
            await ctx.voice_client.disconnect()
    
    @commands.command(name="skip")
    async def skip_song(self, ctx):
        if ctx.voice_client is None:
            embed=Embed(
                title="Error",
                description="Dex is not in any voice channel",
                colour=0xff0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():   
                async with ctx.typing(): 
                    embed = Embed(
                        title = "Skipping",
                        colour = 0x00ff00,
                        timestamp=datetime.utcnow()
                    )
                    player = self.currently_playing_player
                    embed.set_thumbnail(url="https://user-images.githubusercontent.com/63065397/156735015-d12baec8-3ea9-4d23-a577-ebdcb3909566.png")
                    embed.set_author(name=player.title, url=player.url, icon_url=ctx.author.avatar_url)
                    embed.add_field(name="Title", value=player.title, inline = False)
                    embed.add_field(name="Requested by", value=ctx.author.mention, inline = False)
                    embed.set_footer(text="skip requested by "+ctx.author.name)
                await ctx.send(embed=embed)
                if ctx.voice_client.is_playing():
                    ctx.voice_client.stop()
                    await self.keep_playing(ctx)
                else:
                    ctx.voice_client.stop()
                    await self.keep_playing(ctx)
                    ctx.voice_client.pause()
                    

def setup(bot):
    bot.add_cog(Music(bot))