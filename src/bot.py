import discord
import os
import asyncpg
import difflib
from datetime import datetime
from discord.ext import commands, tasks


class Bot(commands.Bot):

    CC_LOGO_URL = 'https://avatars.githubusercontent.com/u/63065397?v=4'
    INTRO_IMG_URL = 'https://user-images.githubusercontent.com/63065397/156466208-ffb6db84-f0c0-4860-ab6d-48ad0f2cd5f7.png'
    EXHAUSTED_FACE = 'https://user-images.githubusercontent.com/63065397/156922064-95c73c2a-b6cb-402e-b24b-d79fe7bf520a.png'
    DEX_YELLOW = 0x8e38ce
    REPOSITORY_URL = 'https://github.com/code-chaser/dex/'

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self.get_pref,
            help_command=None,
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="$dex help",
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
        return

    async def startup(self):
        print("\nINSIDE Bot.startup()\n")
        await self.connect_to_db()
        await self.clone_database()
        await self.wait_until_ready()
        name = "$dex help"
        await self.change_presence(activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=name
        ))
        # self.activity_updates.start()
        print("\n\n len(self.guilds) = " + str(len(self.guilds)) + "\n\n")
        # for guild in self.guilds:
        #     embed = discord.Embed(
        #         title="**NEW UPDATE**",
        #         description="**[*dex*]("+self.REPOSITORY_URL+") version 2.1.1**",
        #         color=self.DEX_YELLOW,
        #         timestamp=datetime.utcnow()
        #     )
        #     changes1 = "**`1.`**: *Help Menu is customized; Use* `"+self.DATABASE['guilds'][str(guild.id)]['prefix']+"help` *to check it out!*\n"
        #     changes2 = "**`2.`**: *Command* `changepref` *is now changed to just* `prefix` *(though the former is still valid);*\n"
        #     changes3 = "**`3.`**: *Command* `prefixspace` *got a new alias* `prefspc`*;*\n"
        #     embed.add_field(
        #         name="**Changes**",
        #         value=changes1+changes2+changes3,
        #         inline=False
        #     )
        #     embed.set_author(icon_url=self.CC_LOGO_URL,
        #                      name="|  codechaser#0647", url=self.REPOSITORY_URL)
        #     general = None
        #     for channel in guild.text_channels:
        #         if channel.permissions_for(guild.me).send_messages:
        #             general = channel
        #     if general is not None:
        #         await general.send(embed=embed)

    # @tasks.loop(seconds=272727)
    # async def activity_updates(self):
    #     user_count = 0
    #     for g in self.guilds:
    #         user_count += len(g.members)

    #     name = "$dex help"
    #     await self.change_presence(activity=discord.Activity(
    #         type=discord.ActivityType.listening,
    #         name=name
    #     ))

    def get_pref(self, _, message):
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
        if type(message.channel) is discord.VoiceChannel:
            embed = discord.Embed(
                description="**You are highly recommended to use DEX in normal text channels, rather than voice dedicated text channels to avoid any unexpected behaviour**",
                color=0xff0000,
                timestamp=datetime.utcnow()
            )
            embed.set_author(
                icon_url=message.author.avatar_url,
                name="| WARNING"
            )
            message.channel.send(embed=embed, reference=message)
        if message.author.bot:
            return
        tag_switch = self.DATABASE['guilds'][str(
            message.guild.id)]['tag_messages']
        target = message.author
        if target == self.user:
            return
        print("\n\n-----------------------\n-----------------------\n\n" +
              str(message.content) + "\n-----------------------\n")
        if tag_switch == 'off':
            return
        if len(message.embeds) > 0:
            for embed in message.embeds:
                embed.set_footer(text=embed.footer.text +
                                 " | Sent by: " + message.author.name)
                await message.channel.send(embed=embed)
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
            server_prefix = self.DATABASE['guilds'][str(
                ctx.guild.id)]['prefix']
            given_command = ctx.message.content[len(server_prefix):]
            given_command = given_command.split(' ')[0]
            closest_match = difflib.get_close_matches(given_command, [k.name for k in self.commands] + [
                                                      alias for command in self.commands for alias in command.aliases], 1, 0.8)
            if len(closest_match) > 0:
                with ctx.typing():
                    embed = discord.Embed(
                        colour=0x00ff00, description="Guessing you meant this: `" + server_prefix + closest_match[0] + "`")
                await ctx.send(reference=ctx.message, embed=embed)
                ctx.message.content = ctx.message.content.replace(
                    given_command, closest_match[0])
                self.process_commands(ctx.message)
                return
            did_you_mean = ', '.join(f'`{match}`' for match in (difflib.get_close_matches(given_command, [
                                     k.name for k in self.commands] + [alias for command in self.commands for alias in command.aliases])))
            v = 'Invalid Command'
            if len(did_you_mean) > 0:
                v += '\nDid you mean: ' + did_you_mean
        else:
            raise error
        embed.add_field(name=n, value=v, inline=False)
        await ctx.send(reference=ctx.message, embed=embed)

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
