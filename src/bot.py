import discord
import json
import os
from discord.ext import commands
import datetime


class Bot(commands.Bot):
    
    CC_LOGO_URL = 'https://avatars.githubusercontent.com/u/63065397?v=4'
    INTRO_IMG_URL = 'https://user-images.githubusercontent.com/63065397/156466208-ffb6db84-f0c0-4860-ab6d-48ad0f2cd5f7.png'
    EXHAUSTED_FACE = 'https://user-images.githubusercontent.com/63065397/156922064-95c73c2a-b6cb-402e-b24b-d79fe7bf520a.png'
    DEX_YELLOW = 0x8e38ce
    REPOSITORY_URL = 'https://github.com/code-chaser/dex/'

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=get_prefix,
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

    async def get_prefix(self, bot, message):
        with open('./data/prefixes.json', 'r') as pref:
            prefixes = json.load(pref)
        print(prefixes[str(message.guild.id)]+"\n\n")
        return prefixes[str(message.guild.id)] + ' '

    def run(self):
        super().run(os.getenv('BOT_TOKEN'))

    async def on_ready(self) -> None:
        print('Logged in as {0.user}'.format(self))
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Stop WW3!', start=datetime.datetime(2022, 2, 24)))

    async def on_guild_join(self, guild) -> None:
        with open('./data/prefixes.json', 'r') as pref:
            prefixes = json.load(pref)
        prefixes[str(guild.id)] = '$dex'
        with open('./data/prefixes.json', 'w') as pref:
            json.dump(prefixes, pref, indent=4)
        with open('./data/tag_messages.json', 'r') as tag_:
            tag_messages = json.load(tag_)
        tag_messages[str(guild.id)] = 'on'
        with open('./data/tag_messages.json', 'w') as tag_:
            json.dump(tag_messages, tag_, indent=4)
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                general = channel
        if general is not None:
            await general.send(embed=self.intro_msg_embed(guild))

    async def on_guild_remove(self, guild) -> None:
        with open('./data/prefixes.json', 'r') as pref:
            prefixes = json.load(pref)
        if str(guild.id) in prefixes.keys():
            prefixes.pop(str(guild.id))
        with open('./data/prefixes.json', 'w') as pref:
            json.dump(prefixes, pref, indent=4)
        with open('./data/tag_messages.json', 'r') as tag_:
            tag_messages = json.load(tag_)
        if str(guild.id) in tag_messages.keys():
            tag_messages.pop(str(guild.id))
        with open('./data/tag_messages.json', 'w') as tag_:
            json.dump(tag_messages, tag_, indent=4)

    async def on_message(self, message) -> None:
        with open('./data/tag_messages.json', 'r') as tag_:
            tag_messages = json.load(tag_)
        if tag_messages[str(message.guild.id)] == 'off':
            return
        target = message.author
        if target == self.user or target.bot:
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
            return
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
            color=0x8e38ce,
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
