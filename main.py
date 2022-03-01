import discord
import json
import os
import cogs.info as info
import cogs.modset as modset
import cogs.report as report
import cogs.fun as fun
import cogs.music as music
from datetime import datetime
from typing import Optional

cogs_list = [info,modset,report,fun,music]

def get_prefix(client, message):
    with open('./data/prefixes.json', 'r') as pref:
        prefixes = json.load(pref)
    return prefixes[str(message.guild.id)] + ' '
    
intents = discord.Intents.all()

client = discord.ext.commands.Bot(command_prefix = get_prefix, intents = intents)

for cog in cogs_list:
    cog.setup(client)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = 'Stop WW3!'))
    
@client.event
async def on_guild_join(guild):
    with open('./data/prefixes.json', 'r') as pref:
        prefixes = json.load(pref)
    prefixes[str(guild.id)] = '$dex'
    with open('./data/prefixes.json', 'w') as pref:
        json.dump(prefixes, pref, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open('./data/prefixes.json', 'r') as pref:
        prefixes = json.load(pref)
    if str(guild.id) in prefixes.keys():
        prefixes.pop(str(guild.id))
    with open('./data/prefixes.json', 'w') as pref:
        json.dump(prefixes, pref, indent = 4)

client.run(os.getenv('BOT_TOKEN'))