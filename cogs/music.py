import discord
import youtube_dl
from typing import Optional
from datetime import datetime
from discord import Embed, Member, Guild
from discord.ext.commands import Cog
from discord.ext.commands import command
from youtube_dl import YoutubeDL

class Music(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue=[]
        self.ydl_options={'format':'bestaudio', 'noplaylist':'True'}
        self.ffmpeg_options={'before_options':'-reconnect 1 -reconnect_streamed 1 - reconnect_delay_max 5', 'options':'-vn'}

    @command(name="join", aliases=["connect"])
    async def join_vc(self, ctx):
        if ctx.author.voice is None:
            embed=Embed(
                title="Error",
                description="User is not in a voice channel",
                colour=0xff0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return False
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
            return True

    @command(name="leave", aliases=["disconnect"])
    async def leave_vc(self, ctx):
        if self.bot.user.voice is None:
            embed=Embed(
                title="Error",
                description="Dex is not in any voice channel",
                colour=0xff0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            await self.bot.user.voice.channel.disconnect()

    def search_yt(self, item):
        with YoutubeDL(self.ydl_options) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item,download = False)['entries'][0]
            except Exception:
                return False
        return {'source':info['formats'][0]['url'], 'title':info['title']}
        
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            voice_channel = self.music_queue[0][1]
            self.music_queue.pop(0)
            source = await discord.FFmpegPCMAudio(m_url,**self.FFMPEG_OPTIONS)
            voice_channel.play(source, after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if self.bot.user.voice is None:
                await self.music_queue[0][1].connect()
            elif self.bot.user.voice.channel != self.music_queue[0][1]
                ctx.voice_client.move_to(self.music_queue[0][1])
            voice_channel = self.music_queue[0][1]
            self.music_queue.pop(0)
            source = await discord.FFmpegPCMAudio.from_probe(m_url,**self.FFMPEG_OPTIONS)
            voice_channel.play(source, after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @command(name="play", aliases=["p"])
    async def play(self, ctx, keyword):
        if not self.join_vc(ctx):
            return
        song = self.search_yt(keyword)
        if type(song) == type(False):
            embed = Embed(
                title="Status",
                colour=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Error",value="Failed to query YouTube for the song",inline=False)
            embed.set_footer(text="Might be due to a livestream or a playlist")
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="Status",
                colour=0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Done",value="Song added to the queue",inline=False)
            self.music_queue.append([song,ctx.author.voice_channel])
            await ctx.send(embed=embed)
            if not self.is_playing:
                await self.play_music()
        

def setup(bot):
    bot.add_cog(Info(bot))