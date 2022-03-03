import discord
import youtube_dl
import ffmpeg
import wavelink
from typing import Optional
from datetime import datetime
from discord import Embed, Member, Guild
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    """Music cog to hold Wavelink related commands and listeners."""
    
    # copied from: https://github.com/PythonistaGuild/Wavelink#getting-started

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to our Lavalink nodes."""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=bot,
                                            host='0.0.0.0',
                                            port=2333,
                                            password='YOUR_LAVALINK_PASSWORD')

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Event fired when a node has finished connecting."""
        print(f'Node: <{node.identifier}> is ready!')

    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        """Play a song with the given search query.

        If not connected, connect to our voice channel.
        """
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.play(search)

def setup(bot):
    bot.add_cog(Music(bot))