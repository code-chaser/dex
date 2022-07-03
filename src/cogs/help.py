import discord
from typing import Optional
from discord.ext import commands


class Help(commands.Cog):
    commands_descriptions = {
        "Music": {
            "join": ["Joins the voice channel of the author", ["connect"]],
            "leave": ["Leaves if connected to any voice channel", ["disconnect", "dc"]],
            "play": ["Streams a song directly from youtube", ["stream", "p", "add"]],
            "playm": ["Streams multiple songs (seperated by semicolons ';')", ["streamm", "pm", "addm"]],
            "dplay": ["Downloads a song and then queues it to reduce any possible lags", []],
            "dplaym": ["'dplays' multiple songs (seperated by semicolons ';')", []],
            "loop": ["Toggles looping of the queue", []],
            "repeat": ["Toggles repeating of the currently playing song", []],
            "restart": ["Restarts the currently playing song", []],
            "queue": ["Shows the current queue", ["view"]],
            "remove": ["Removes given song from the queue, takes song position as arguement", []],
            "jump": ["Jumps to given song in the queue, takes song position as arguement", ["jumpto"]],
            "volume": ["Sets the volume of the player to given value", ["vol"]],
            "stop": ["Stops the music and clears the queue", ["stfu", "shut"]],
            "pause": ["Pauses the player", []],
            "resume": ["Resumes the player", []],
            "next": ["Plays the next song in the queue", ["skip"]],
            "previous": ["Plays the previous song in the queue", ["prev"]],
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
            "changepref": ["Changes the prefix for the server to the appended string", ["changeprefix"]],
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
        "Help": {
            "help": ["Shows this message", []]
        },
    }
            
            
    def __init__(self, bot):
        self.bot = bot
    # ----------------------------------------------------------------------------------------------------------------------

    async def show_help(self, ctx):
        
        return

    @commands.command(name="help", aliases=["?"], help="shows the list of valid commands")
    async def help_command(self, ctx, command_name: Optional[str]):
        if command_name is None:
            await self.show_help(ctx)
            return
        
        return
    
    # ----------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(Help(bot))
