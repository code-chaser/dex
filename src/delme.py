import json
import os
import datetime

import discord
from discord.ext import commands

exhausted_face = "https://user-images.githubusercontent.com/63065397/156922064-95c73c2a-b6cb-402e-b24b-d79fe7bf520a.png"


class Bot(commands.Bot):
    """
    a simple bot subclass
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            command_prefix=self.get_prefix,
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="Stop WW3!",
                large_image_url=exhausted_face,
                small_image_url=exhausted_face,
                start=datetime.datetime(2022, 2, 24),
            ),
        )  # just calling the init of the parent class (commands.Bot)

        self.setup()

    async def get_prefix(self, message):
        with open("./data/prefixes.json", "r") as pref:
            prefixes = json.load(pref)
        print(prefixes[str(message.guild.id)]+"\n\n")
        return prefixes[str(message.guild.id)] + " "

    def setup(self) -> None:
        """
        setting up the bot which entails
        loading all cogs and printing info.
        """

        for _file in os.listdir("src/cogs"):  # _file is the name of each file in the cogs dir
            if not _file.startswith("_"):  # make sure it doesnt load __pycache__
                self.load_extension(f"src.cogs.{_file[:-3]}")  # load the cog

    def run(self) -> None:
        TOKEN = os.environ["BOT_TOKEN"]
        super().run(TOKEN)  # just to keep main.py even more tidy

    async def on_ready(self) -> None:
        print("Logged in as {0.user}".format(self))

    async def on_guild_join(self, guild: discord.Guild) -> None:
        with open("./data/prefixes.json", "r") as pref:
            prefixes = json.load(pref)

        prefixes[str(guild.id)] = "$dex"
        with open("./data/prefixes.json", "w") as pref:
            json.dump(prefixes, pref, indent=4)

    async def on_guild_remove(self, guild: discord.Guild) -> None:
        with open("./data/prefixes.json", "r") as pref:
            prefixes = json.load(pref)

        if str(guild.id) in prefixes.keys():
            prefixes.pop(str(guild.id))
        with open("./data/prefixes.json", "w") as pref:
            json.dump(prefixes, pref, indent=4)