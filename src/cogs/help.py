import discord
from datetime import datetime
from typing import Optional
from discord.ext import commands, tasks


class Help(commands.Cog):
    commands_description = {
        "Music - Basic": {
            "join": ["Joins the voice channel of the author", ["connect"]],
            "leave": ["Leaves if connected to any voice channel", ["disconnect", "dc"]],
            "play": ["Streams a song directly from youtube", ["stream", "p", "add"]],
            "playm": ["Streams multiple songs (seperated by semicolons ';')", ["streamm", "pm", "addm"]],
            "dplay": ["Downloads a song and then queues it to reduce any possible lags", []],
            "dplaym": ["'dplays' multiple songs (seperated by semicolons ';')", []]
        },
        "Music - Player Controls": {
            "queue": ["Shows the current queue", ["view"]],
            "stop": ["Stops the music and clears the queue", ["stfu", "shut"]],
            "pause": ["Pauses the player", []],
            "resume": ["Resumes the player", []],
            "volume": ["Sets the volume of the player to given value", ["vol"]],
            "next": ["Plays the next song in the queue", ["skip"]],
            "previous": ["Plays the previous song in the queue", ["prev"]],
            "loop": ["Toggles looping of the queue", []],
            "repeat": ["Toggles repeating of the currently playing song", []],
            "restart": ["Restarts the currently playing song", []],
            "remove": ["Removes given song from the queue, takes song position as arguement", []],
            "jump": ["Jumps to given song in the queue, takes song position as arguement", ["jumpto"]],
            "lyrics": ["Shows the lyrics of the currently playing song", []]
        },
        "Fun": {
            "inspire": ["Sends a random inspirational quote", ["iquote"]],
            "apod": ["Sends astronomy pic of the day from NASA", ["napod", "astropic", "astropicotd"]],
            "meme": ["Sends a random meme", ["hehe"]],
            "reddit": ["Shows top headlines of the given subreddit", ["subreddit"]],
        },
        "Mod Settings": {
            "tags": ["Toggles tagging messages feature", ["tagging", "msgtags"]],
            "prefix": ["Changes the prefix for the server to the appended string", ["changeprefix", "changepref"]],
            "prefixspace": ["Toggles the trailing space in the prefix", ["prefspace", "prefspc"]],
            "goodbye!": ["Leaves the server", ["leaveThisServer"]],
            "madeby?": ["Show information about the creator of the bot", []]
        },
        "Codeforces": {
            "cf-handle": ["Shows details of the requested codeforces handle", ["cf-user"]]
        },
        "Info": {
            "userinfo": ["Shows info about the requested user, or the author of the message if no or invalid user is specified", ["ui", "memberinfo", "mi"]],
            "serverinfo": ["Shows info about the server", ["si", "guildinfo", "gi"]]
        },
        "Other": {
            "covid19": ["Shows the current covid19 stats of the given nation, or global if no nation provided", []],
            "ping": ["Shows the latency of the bot", ["latency"]]
        },
        "Help": {
            "help": ["Shows description of commands", []],
            "user-manual": ["Shows paginated description of commands", ["paginated-help", "help-pages"]]
        }
    }
    reactions = {
        "first": "⏮",
        "back": "◀️",
        "forward": "▶️",
        "last": "⏭"
    }
    # ----------------------------------------------------------------------------------------------------------------------

    def __init__(self, bot):
        self.bot = bot
        self.embeds_list = []
        for category, commands_dict in self.commands_description.items():
            self.embeds_list.append(discord.Embed(
                title="Help: " + category,
                description="",
                color=self.bot.DEX_YELLOW,
                timestamp=datetime.utcnow(),
            ))
            for command, description in commands_dict.items():
                self.embeds_list[-1].add_field(name="`"+command +
                                               "`", value=description[0], inline=False)
            self.embeds_list[-1].set_footer(text="Page " + str(
                len(self.embeds_list)) + " of " + str(len(self.commands_description)) + "\nUse reactions below as buttons to navigate ")
    # ----------------------------------------------------------------------------------------------------------------------
    
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     for guild in self.bot.guilds:
    #         count = 0
    #         if str(guild.id) in ['801427258090192946','802197877039956008']:
    #             count = 2
    #         spam_channels = []
    #         for channel in guild.text_channels:
    #             name = str(channel.name).lower()
    #             if (name.count("spam", 0, len(name)) + name.count("music", 0, len(name)) + name.count("bot", 0, len(name)) > 0):
    #                 spam_channels.append(channel)
            
    #         for channel in spam_channels:
    #             if count == 3:
    #                 break
    #             if channel.permissions_for(guild.me).send_messages & channel.permissions_for(guild.me).read_messages & channel.permissions_for(guild.me).manage_messages & channel.permissions_for(guild.me).add_reactions:
    #                 count += 1
    #                 async with channel.typing():
    #                     self.embeds_list[0].set_author(icon_url=guild.icon_url, name="|  " +
    #                                                 self.bot.DATABASE['guilds'][str(guild.id)]['prefix'] + "user-manual")
    #                 msg = await channel.send(embed=self.embeds_list[0])
    #                 if msg is not None:
    #                     for name, reaction in self.reactions.items():
    #                         await msg.add_reaction(reaction)
                    
    #         for channel in guild.text_channels:
    #             if count == 3:
    #                 break
    #             if channel in spam_channels:
    #                 continue
    #             if channel.permissions_for(guild.me).send_messages:
    #                 count += 1
    #                 async with channel.typing():
    #                     self.embeds_list[0].set_author(icon_url=guild.icon_url, name="|  " +
    #                                                 self.bot.DATABASE['guilds'][str(guild.id)]['prefix'] + "user-manual")
    #                 msg = await channel.send(embed=self.embeds_list[0])
    #                 if msg is not None:
    #                     for name, reaction in self.reactions.items():
    #                         await msg.add_reaction(reaction)
    #     return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction = str(payload.emoji)
        user = self.bot.get_user(payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        print("\nreaction added to a message authored by " + str(message.author) + "\n")
        if user == self.bot.user:
            return
        if message.author != self.bot.user:
            return
        if len(message.embeds) == 0:
            return
        if (not message.embeds[0].title.startswith("Help: ")) or (message.embeds[0].title == "Help: All"):
            return
        page = int(message.embeds[0].footer.text.split(" ")[1]) - 1
        if reaction == self.reactions["first"]:
            page = 0
        elif reaction == self.reactions["back"]:
            page -= 1
        elif reaction == self.reactions["forward"]:
            page += 1
        elif reaction == self.reactions["last"]:
            page = len(self.embeds_list) - 1
        page %= len(self.embeds_list)
        self.embeds_list[page].set_author(icon_url=user.avatar_url, name="|  " +
                                          self.bot.DATABASE['guilds'][str(message.guild.id)]['prefix'] + "user-manual")
        await message.edit(embed=self.embeds_list[page])
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        reaction = str(payload.emoji)
        user = self.bot.get_user(payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        print("\nreaction removed from a message authored by " + str(message.author) + "\n")
        if user == self.bot.user:
            return
        if message.author != self.bot.user:
            return
        if len(message.embeds) == 0:
            return
        if (not message.embeds[0].title.startswith("Help: ")) or (message.embeds[0].title == "Help: All"):
            return
        page = int(message.embeds[0].footer.text.split(" ")[1]) - 1
        if reaction == self.reactions["first"]:
            page = 0
        elif reaction == self.reactions["back"]:
            page -= 1
        elif reaction == self.reactions["forward"]:
            page += 1
        elif reaction == self.reactions["last"]:
            page = len(self.embeds_list) - 1
        page %= len(self.embeds_list)
        self.embeds_list[page].set_author(icon_url=user.avatar_url, name="|  " +
                                          self.bot.DATABASE['guilds'][str(message.guild.id)]['prefix'] + "user-manual")
        await message.edit(embed=self.embeds_list[page])
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="user-manual", aliases=["paginated-help", "help-pages"], help="Shows paginated description of commands")
    async def user_manual_command(self, ctx, page: Optional[int] = 1):
        if page is None:
            page = 1
        elif (page < 1) or (page > len(self.embeds_list)):
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description="Invalid page number!\nPage number must be between 1 & " + str(len(self.embeds_list)),
                    color=0xFF0000,
                    timestamp=datetime.utcnow(),
                )
            await ctx.reply(embed=embed)
            return
        page -= 1
        async with ctx.typing():
            self.embeds_list[page].set_author(icon_url=ctx.author.avatar_url, name="|  " +
                                          self.bot.DATABASE['guilds'][str(ctx.guild.id)]['prefix'] + "user-manual")
        msg = await ctx.reply(embed=self.embeds_list[page])
        for name, reaction in self.reactions.items():
            await msg.add_reaction(reaction)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    async def all_help(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title="Help: All",
                description="",
                color=self.bot.DEX_YELLOW,
                timestamp=datetime.utcnow(),
            )

            for category in self.commands_description.keys():
                embed.add_field(name='**'+category+'**', value="\n".join(["**`{}`** - *{}*".format(
                    command, description[0]) for command, description in self.commands_description[category].items()]), inline=False)
            embed.set_footer(
                text="Use `help <command>` to get more info about a command"
            )
            embed.set_author(icon_url=ctx.author.avatar_url, name="|  " +
                             self.bot.DATABASE['guilds'][str(ctx.guild.id)]['prefix'] + "help")
        await ctx.reply(embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    @commands.command(name="help", aliases=["?"], help="Shows the list of valid commands")
    async def help_command(self, ctx, command_name: Optional[str]):
        if command_name is None:
            await self.all_help(ctx)
            return
        invalid = True
        category = None
        for key in self.commands_description.keys():
            for sub_key in self.commands_description[key].keys():
                if (command_name in self.commands_description[key][sub_key][1]) or (sub_key == command_name):
                    invalid = False
                    command_name = sub_key
                    category = key
                    break
        if invalid:
            async with ctx.typing():
                embed = discord.Embed(
                    title="Error",
                    description="Invalid command\nUse `" + self.bot.DATABASE['guilds'][str(
                        ctx.guild.id)]['prefix'] + "help` to see the list of valid commands",
                    color=0xff0000,
                    timestamp=datetime.utcnow()
                )
                embed.set_author(icon_url=ctx.author.avatar_url, name="|  " +
                                 self.bot.DATABASE['guilds'][str(ctx.guild.id)]['prefix'] + "help " + command_name)
            await ctx.reply(embed=embed)
            return
        async with ctx.typing():
            embed = discord.Embed(
                title="Help: " + category + ": `" + command_name + "`",
                description="",
                color=self.bot.DEX_YELLOW,
                timestamp=datetime.utcnow()
            )
            embed.add_field(
                name="Description", value=self.commands_description[category][command_name][0], inline=False)
            aliases_string = "None"
            if len(self.commands_description[category][command_name][1]) > 0:
                aliases_string = "["
                for i in range(0, len(self.commands_description[category][command_name][1])):
                    aliases_string += "`" + \
                        self.commands_description[category][command_name][1][i] + "`"
                    if i != len(self.commands_description[category][command_name][1]) - 1:
                        aliases_string += ", "
                aliases_string += "]"
            embed.add_field(name="Aliases", value=aliases_string, inline=False)
            embed.set_footer(text="Use `"+self.bot.DATABASE['guilds'][str(
                ctx.guild.id)]['prefix']+"help` to get description of all commands")
            embed.set_author(icon_url=ctx.author.avatar_url, name="|  " +
                             self.bot.DATABASE['guilds'][str(ctx.guild.id)]['prefix'] + "help " + command_name)
        await ctx.reply(embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Help(bot))
