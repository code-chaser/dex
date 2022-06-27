import discord
import os
import asyncpg
from datetime import datetime
from discord.ext import commands


class Bot(commands.Bot):

    CC_LOGO_URL = 'https://avatars.githubusercontent.com/u/63065397?v=4'
    INTRO_IMG_URL = 'https://user-images.githubusercontent.com/63065397/156466208-ffb6db84-f0c0-4860-ab6d-48ad0f2cd5f7.png'
    EXHAUSTED_FACE = 'https://user-images.githubusercontent.com/63065397/156922064-95c73c2a-b6cb-402e-b24b-d79fe7bf520a.png'
    DEX_YELLOW = 0x8e38ce
    REPOSITORY_URL = 'https://github.com/code-chaser/dex/'

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix,
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="$dex help",
                large_image_url=self.EXHAUSTED_FACE,
                small_image_url=self.EXHAUSTED_FACE,
                start=datetime(2022, 2, 24),
            ),
        )
        self.DB_CONNECTION = None
        self.DATABASE = {}
        self.loop.create_task(self.startup())

        for file in os.listdir('./src/cogs'):
            if file.endswith('.py'):
                self.load_extension(f'src.cogs.{file[:-3]}')

    async def connect_to_db(self) -> None:
        self.DB_CONNECTION = await asyncpg.connect(
            host=os.getenv('DEX_DB_HOST'),
            database=os.getenv('DEX_DB_NAME'),
            user=os.getenv('DEX_DB_USER'),
            port=os.getenv('DEX_DB_PORT'),
            password=os.getenv('DEX_DB_PASSWORD')
        )
        print("\nDATABASE CONNECTED\n")

    async def clone_database(self):
        await self.DB_CONNECTION.execute('CREATE TABLE IF NOT EXISTS guilds (guild_id VARCHAR(27) NOT NULL, prefix VARCHAR(108) NOT NULL, tag_messages SWITCH NOT NULL, PRIMARY KEY (guild_id));')
        self.DATABASE['guilds'] = {}
        self.DATABASE['guilds'] = {result['guild_id']: {k: v for k, v in result.items() if k != 'guild_id'} for result in await self.DB_CONNECTION.fetch("SELECT * FROM guilds")}
        print("\nDATABASE CLONED\n")
        print("\n\n****DATABASE DICTIONARY****\n\n")
        print(self.DATABASE)
        print("\n\n")
        return

    async def startup(self):
        print("\nINSIDE Bot.startup()\n")
        await self.connect_to_db()
        await self.clone_database()
        self.command_prefix = self.get_prefix

    def get_prefix(self, message):
        return self.DATABASE['guilds'][str(message.guild.id)]['prefix']

    def run(self) -> None:
        super().run(os.getenv('DEX_BOT_TOKEN'))

    async def on_ready(self):
        print('Logged in as {0.user}'.format(self))

    async def on_guild_join(self, guild):
        if str(guild.id) in self.DATABASE['guilds'].keys():
            return
        await self.DB_CONNECTION.execute('INSERT INTO guilds (guild_id,prefix,tag_messages) VALUES (\'' +
                                         str(guild.id)+'\', \'$dex \', \'on\');')
        self.DATABASE['guilds'][str(guild.id)] = {}
        self.DATABASE['guilds'][str(guild.id)] = {
            'prefix': '$dex ', 'tag_messages': 'on'}
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                general = channel
        if general is not None:
            await general.send(embed=self.intro_msg_embed(guild))
        return

    async def on_guild_remove(self, guild):
        await self.DB_CONNECTION.execute('DELETE FROM guilds WHERE guild_id = \'' +
                                         str(guild.id) + '\';')
        if str(guild.id) in self.DATABASE['guilds'].keys():
            self.DATABASE['guilds'].pop(str(guild.id))
        return

    async def on_message(self, message):
        await self.process_commands(message)
        tag_switch = self.DATABASE['guilds'][str(
            message.guild.id)]['tag_messages']
        target = message.author
        if target == self.user:
            return
        print("\n\n-----------------------\n-----------------------\n\n" +
              str(message.content) + "\n-----------------------\n")
        if tag_switch == 'off':
            return
        embed = discord.Embed(
            title='Message Tagged',
            colour=target.colour,
            timestamp=datetime.utcnow(),
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
            timestamp=datetime.utcnow(),
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
        description = ('\nThanks for adding me to ' + guild.name + '!')
        description += ('\nUse `$dex help` to get started!')
        description += ('\nSource Code: [Link](')
        description += (self.REPOSITORY_URL)
        description += (')')
        embed = discord.Embed(
            title='**GREETINGS!**',
            description=description,
            color=self.DEX_YELLOW,
            timestamp=datetime.utcnow(),
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
