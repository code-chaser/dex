import discord
import json
import os
import datetime
import psycopg2
import configparser
from discord.ext import commands


class Bot(commands.Bot):

    CC_LOGO_URL = 'https://avatars.githubusercontent.com/u/63065397?v=4'
    INTRO_IMG_URL = 'https://user-images.githubusercontent.com/63065397/156466208-ffb6db84-f0c0-4860-ab6d-48ad0f2cd5f7.png'
    EXHAUSTED_FACE = 'https://user-images.githubusercontent.com/63065397/156922064-95c73c2a-b6cb-402e-b24b-d79fe7bf520a.png'
    DEX_YELLOW = 0x8e38ce
    REPOSITORY_URL = 'https://github.com/code-chaser/dex/'
    DB_CONNECTION = None

    def __init__(self, *args, **kwargs):
        self.connect_to_db()
        super().__init__(
            command_prefix=self.get_prefix,
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="Stop WW3!",
                large_image_url=self.EXHAUSTED_FACE,
                small_image_url=self.EXHAUSTED_FACE,
                start=datetime.datetime(2022, 2, 24),
            ),
        )

        for file in os.listdir('./src/cogs'):
            if file.endswith('.py'):
                self.load_extension(f'src.cogs.{file[:-3]}')

    def connect_to_db(self) -> None:
        
        self.DB_CONNECTION = psycopg2.connect(
            host=os.getenv('DEX_DB_HOST'),
            database=os.getenv('DEX_DB_NAME'),
            user=os.getenv('DEX_DB_USER'),
            port=os.getenv('DEX_DB_PORT'),
            password=os.getenv('DEX_DB_PASSWORD'),
        )
    
    async def get_prefix(self, message):
        cur = self.DB_CONNECTION.cursor()
        cur.execute('SELECT prefix FROM guilds WHERE guild_id = \'' + str(message.guild.id) + '\';')
        prefix = cur.fetchone()
        return prefix

    def run(self) -> None:
        super().run(os.getenv('BOT_TOKEN'))

    async def on_ready(self):
        print('Logged in as {0.user}'.format(self))
        cur = self.DB_CONNECTION.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS guilds (guild_id VARCHAR(27) NOT NULL, prefix VARCHAR(108) NOT NULL, tag_messages SWITCH NOT NULL, PRIMARY KEY (guild_id));')
        self.DB_CONNECTION.commit()

    async def on_guild_join(self, guild) -> None:
        cur = self.DB_CONNECTION.cursor()
        cur.execute('INSERT INTO guilds (guild_id,prefix,tag_messages) VALUES (\'' + str(guild.id)+'\', \'$dex \', \'on\');')
        self.DB_CONNECTION.commit()
        cur.close()
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                general = channel
        if general is not None:
            await general.send(embed=self.intro_msg_embed(guild))
        return

    async def on_guild_remove(self, guild) -> None:
        cur = self.DB_CONNECTION.cursor()
        cur.execute('DELETE FROM guilds WHERE guild_id = \'' + str(guild.id) + '\';')
        self.DB_CONNECTION.commit()
        cur.close()
        return

    async def on_message(self, message) -> None:
        await self.process_commands(message)
        cur = self.DB_CONNECTION.cursor()
        cur.execute('SELECT tag_messages FROM guilds WHERE guild_id = \'' + str(message.guild.id) + '\';')
        tag_switch = cur.fetchone()
        cur.close()
        if tag_switch[0] == 'off':
            return
        target = message.author
        if target == self.user:
            return
        embed = discord.Embed(
            title='Message Tagged',
            colour=target.colour,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_footer(
            text=''.join('`<prefix> tags off` -to turn this off'),
        )
        embed.add_field(name='Message', value=message.content, inline=False)
        embed.add_field(name='Author', value=target.mention, inline=True)
        embed.set_thumbnail(url=target.avatar_url)
        await message.channel.send(embed=embed)

    async def on_command_error(self, ctx, error) -> None:
        embed = discord.Embed(
            title='Status',
            colour=0xff0000,
            timestamp=datetime.datetime.utcnow(),
        )
        if isinstance(error, commands.MissingPermissions):
            n = 'Error'
            v = 'Missing Permissions'
        elif isinstance(error, commands.MissingRequiredArgument):
            n = 'Error'
            v = 'Missing required arguements'
        elif isinstance(error, commands.MemberNotFound):
            n = 'Error'
            v = "Requested member not found or Dex doesn't have access to them"
        elif isinstance(error, commands.BotMissingPermissions):
            n = 'Error'
            v = 'Missing Permissions'
        elif isinstance(error, commands.CommandNotFound):
            n = 'Error'
            v = 'Invalid Command'
        else:
            raise error
        embed.add_field(name=n, value=v, inline=False)
        await ctx.send(embed=embed)

    def intro_msg_embed(self, guild):
        description = ''
        description = description.join(
            '\nThanks for adding me to ' + guild.name + '!')
        description = description.join('\nUse `$dex help` to get started!')
        description = description.join(
            '\nVisit: '.join(self.REPOSITORY_URL))
        embed = discord.Embed(
            title='**GREETINGS!**',
            description=description,
            color=self.DEX_YELLOW,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_image(url=self.INTRO_IMG_URL)
        embed.set_author(
            name='dex',
            url=self.REPOSITORY_URL,
            icon_url=self.user.avatar_url,
        )
        embed.set_footer(
            text='made by codechaser',
            icon_url=self.CC_LOGO_URL,
        )
        embed.set_thumbnail(url=guild.icon_url)
        return embed
