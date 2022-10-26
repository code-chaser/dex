import discord
import difflib
from datetime import datetime
from typing import Optional
from discord.ext import commands, tasks


class Help(commands.Cog):
    commands_description = {
        "Music - Basic": {
            "join": ["Joins the voice channel of the author", ["connect"], None],
            "leave": ["Leaves if connected to any voice channel", ["disconnect", "dc"], None],
            "play": ["Streams a song directly from youtube", ["stream", "p", "add"], "**`<song-name>`**"],
            "playm": ["Streams multiple songs (seperated by semicolons ';')", ["streamm", "pm", "addm"], "**`<song-name-1>;<song-name-2>;...`**"],
            "dplay": ["Downloads a song and then queues it to reduce any possible lags", [], "**`<song-name>`**"],
            "dplaym": ["'dplays' multiple songs (seperated by semicolons ';')", [], "**`<song-name-1>;<song-name-2>;...`**"],
        },
        "Music - Player Controls": {
            "queue": ["Shows the current queue", ["view"], None],
            "stop": ["Stops the music and clears the queue", ["shut"], None],
            "pause": ["Pauses the player", [], None],
            "resume": ["Resumes the player", [], None],
            "volume": ["Sets the volume of the player to given value", ["vol"], "**`<volume>`**"],
            "next": ["Plays the next song in the queue", ["skip"], None],
            "previous": ["Plays the previous song in the queue", ["prev"], None],
            "loop": ["Toggles looping of the queue", [], None],
            "repeat": ["Toggles repeating of the currently playing song", [], None],
            "restart": ["Restarts the currently playing song", [], None],
            "remove": ["Removes given song from the queue, takes song position as arguement", [], "**`<song-position>`**"],
            "jump": ["Jumps to given song in the queue, takes song position as arguement", ["jumpto"], "**`<song-position>`**"],
            "lyrics": ["Shows the lyrics of the currently playing song", [], "`<song-name>`"],
        },
        "Fun": {
            "inspire": ["Sends a random inspirational quote", ["iquote"], None],
            "apod": ["Sends astronomy pic of the day from NASA", ["napod", "astropic", "astropicotd"], None],
            "meme": ["Sends a random meme", ["hehe"], None],
            "reddit": ["Shows top headlines of the given subreddit", ["subreddit"], "**`<subreddit-name>`**"],
            "crypto": ["Shows the price of given cryptocurrency(s) in given currency(s)", ["cryptocurrency", "crypto-price", "coingecko"], "**`<crypto-1>;<crypto-2>;...`** ` ` `<currency-1>;<currency-2>;...`"],
            "tts": ["Converts given text into speech of given language", ["text-to-speech"], "**`<language> <text>`**"],
            "trivia-cat": ["Sends the complete list of available trivia categories", ["qna-cat", "qna-categories", "trivia-categories"], None],
            "trivia": ["Shows a question of given category id with it's answer", ["q/a", "ask", "question", "qna"], "`<category-id>`"],
        },
        "Mod Settings": {
            "tags": ["Toggles tagging messages feature", ["tagging", "msgtags"], "`<on/off>`"],
            "prefix": ["Changes the prefix for the server to the appended string", ["changeprefix", "changepref"], "`<new-prefix>`"],
            "prefixspace": ["Toggles the trailing space in the prefix", ["prefspace", "prefspc"], "`<on/off>`"],
            "goodbye!": ["Leaves the server", ["leaveThisServer"], None],
            "madeby?": ["Show information about the creator of the bot", [], None],
        },
        "Codeforces": {
            "cf-handle": ["Shows details of the requested codeforces handle", ["cf-user"], "`<username>`"]
        },
        "Info": {
            "userinfo": ["Shows info about the requested user, or the author of the message if no or invalid user is specified", ["ui", "memberinfo", "mi"], "`<tagged-user>`"],
            "serverinfo": ["Shows info about the server", ["si", "guildinfo", "gi"], None]
        },
        "Other": {
            "covid19": ["Shows the current covid19 stats of the given nation, or global if no nation provided", [], "`<nation>`"],
            "ping": ["Shows the latency of the bot", ["latency"], None]
        },
        "Help": {
            "help": ["Shows detailed description of the given command or briefs all commands if none specified", ["?"], "`<command>`"],
            "user-manual": ["Shows paginated description of commands", ["paginated-help", "help-pages"], None]
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
    #         if str(guild.id) in []:
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
        print("\nreaction added to a message authored by " +
              str(message.author) + "\n")
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
        print("\nreaction removed from a message authored by " +
              str(message.author) + "\n")
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
                    description="Invalid page number!\nPage number must be between 1 & " +
                    str(len(self.embeds_list)),
                    color=0xFF0000,
                    timestamp=datetime.utcnow(),
                )
            await ctx.send(reference=ctx.message, embed=embed)
            return
        page -= 1
        async with ctx.typing():
            self.embeds_list[page].set_author(icon_url=ctx.author.avatar_url, name="|  " +
                                              self.bot.DATABASE['guilds'][str(ctx.guild.id)]['prefix'] + "user-manual")
        msg = await ctx.send(reference=ctx.message, embed=self.embeds_list[page])
        for name, reaction in self.reactions.items():
            await msg.add_reaction(reaction)
        return
    # ----------------------------------------------------------------------------------------------------------------------

    async def all_help(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title="Help: All",
                description="**Prefix: `" +
                self.bot.DATABASE['guilds'][str(
                    ctx.guild.id)]['prefix'] + "`**",
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
        await ctx.send(embed=embed, reference=ctx.message)
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
                server_prefix = self.bot.DATABASE['guilds'][str(
                    ctx.guild.id)]['prefix']
                given_command = ctx.message.content[len(server_prefix):]
                given_command = given_command.split(' ')[1]
                did_you_mean = ', '.join(f'`{match}`' for match in (difflib.get_close_matches(given_command, [
                                         k.name for k in self.bot.commands] + [alias for command in self.bot.commands for alias in command.aliases])))
                if did_you_mean is not None:
                    did_you_mean = f'\nDid you mean: {did_you_mean}\n'
                embed = discord.Embed(
                    title="Error",
                    description="Invalid command" + did_you_mean + "\nUse `" + self.bot.DATABASE['guilds'][str(
                        ctx.guild.id)]['prefix'] + "help` to see the list of valid commands",
                    color=0xff0000,
                    timestamp=datetime.utcnow()
                )
                embed.set_author(icon_url=ctx.author.avatar_url, name="|  " +
                                 self.bot.DATABASE['guilds'][str(ctx.guild.id)]['prefix'] + "help " + command_name)
            await ctx.send(reference=ctx.message, embed=embed)
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
            embed.add_field(
                name="Parameters", value=self.commands_description[category][command_name][2] or "None", inline=False)
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
        await ctx.send(reference=ctx.message, embed=embed)
        return
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Help(bot))
