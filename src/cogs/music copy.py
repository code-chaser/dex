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
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.music_queue=[]
        self.bot_voice_client = None
        self.players = {}
        self.ydl_options={
            'format':'bestaudio',
            'noplaylist':True,
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        self.ffmpeg_options={'before_options':'-reconnect 1 -reconnect_streamed 1 - reconnect_delay_max 5', 'options':'-vn'}

    @command(name="join", aliases=["connect"], help = "joins the vc of the command author")
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
                self.bot_voice_client = ctx.voice_client
            else:
                await ctx.voice_client.move_to(voice_channel)
                self.bot_voice_client = ctx.voice_client
            return True

    @command(name="leave", aliases=["disconnect"], help="leaves if connected to any vc")
    async def leave_vc(self, ctx):
        if ctx.voice_client is None:
            embed=Embed(
                title="Error",
                description="Dex is not in any voice channel",
                colour=0xff0000,
                timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
        else:
            await ctx.guild.voice_client.disconnect()
            self.bot_voice_client = None

    def search_yt(self, item):
        with YoutubeDL(self.ydl_options) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item,download = False)['entries'][0]
            except Exception:
                return False
        return {'source':info['formats'][0]['url'], 'title':info['title']}
        
    def play_next(self,ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            self.bot_voice_client = ctx.voice_client
            self.music_queue.pop(0)
            source = discord.FFmpegOpusAudio(m_url,**self.ffmpeg_options)
            ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))
        else:
            self.is_playing = False

    async def play_music(self,ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            if ctx.guild.voice_client is None:
                await self.music_queue[0][1].connect()
            elif ctx.guild.voice_client.channel != self.music_queue[0][1]:
                ctx.voice_client.move_to(self.music_queue[0][1])
            self.bot_voice_client = ctx.voice_client
            self.music_queue.pop(0)
            source = discord.FFmpegOpusAudio(m_url,**self.ffmpeg_options)
            ctx.voice_client.play(source, after=lambda e: self.play_next(ctx))
        else:
            self.is_playing = False

    @command(name="play", aliases=["p"], help = "apparently, replit won't let it play!")
    async def play(self, ctx, keyword):
        # embed = Embed(
        #         title="Status",
        #         colour=0xff0000,
        #         timestamp=datetime.utcnow()
        #     )
        # embed.add_field(name="Error",value="Replit's not letting me play! T_T",inline=False)
        # 
        # await ctx.send(embed=embed)
        # return
        await self.join_vc(ctx)
        if ctx.author.voice is None:
            return
        song = self.search_yt(keyword)
        if type(song) == type(False):
            embed = Embed(
                title="Status",
                colour=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Error",value="Failed to query YouTube for the music",inline=False)
            embed.set_footer(text="Might be due to a livestream or a playlist")
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                title="Status",
                colour=0x00ff00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Done",value="Song added to the queue",inline=False)
            self.music_queue.append([song,ctx.author.voice.channel,ctx.author])
            await ctx.send(embed=embed)
            player = await ctx.voice_client.create_ytdl_player(song['source'])
            self.players[ctx.guild.id] = player
            player.start()
            # if not self.is_playing:
            #     await self.play_music(ctx)
        

def setup(bot):
    bot.add_cog(Music(bot))