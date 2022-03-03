import discord
import youtube_dl
import ffmpeg
from typing import Optional
from datetime import datetime
from discord import Embed, Member, Guild
from discord.ext.commands import Cog
from discord.ext.commands import command
from youtube_dl import YoutubeDL

class Music(Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @command(name="join", aliases=["connect"], help = "joins the vc of the command author")
    async def join_vc(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("User is not in a voice channel")
            return False
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        return True

    @command(name="leave", aliases=["disconnect"], help="leaves if connected to any vc")
    async def leave_vc(self, ctx):
        await ctx.voice.disconnect()
        
    @command(name="play", aliases=["p"], help="plays a song from youtube")
    async def play(self,ctx,url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 - reconnect_delay_max 5', 'options':'-vn'}
        YDL_OPTIONS = {'format':'bestaudio'}
        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 =  info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

def setup(bot):
    bot.add_cog(Music(bot))