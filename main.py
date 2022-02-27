import discord
from discord.ext import commands
import os
import requests
import json
from replit import db

def get_prefix(client, message):
    with open('./data/prefixes.json', 'r') as pref:
        prefixes = json.load(pref)
    return prefixes[str(message.guild.id)] + ' '
    
client = commands.Bot(command_prefix = get_prefix)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    member_count = 0
    bot_count = 0
    for g in client.guilds:
        member_count += len(g.members)
        for m in g.members:
            print(m)
            print("\n")
            if m.bot:
                bot_count += 1
    
    channel = client.get_channel(int(os.environ['CONSOLE_CHANNEL_ID']))
    await channel.send("Logged in!\nOnline Now!\n\nWatching " + str(len(client.guilds)) + " servers\nwith " + str(member_count) + " members including " + str(bot_count) + " bots\n")
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

def get_quote():
    response = requests.get("https://zenquotes.io/api//random")
    quote_json = json.loads(response.text)
    quote = "\"" + quote_json[0]['q'] + "\" -" + quote_json[0]['a']
    return (quote)

@client.command()
async def changeprefix(ctx, prefix):
    with open('./data/prefixes.json', 'r') as pref:
        prefixes = json.load(pref)
    prefixes[str(ctx.guild.id)] = prefix
    await ctx.send("Prefix changed!\nNew Prefix is " + prefix)
    with open('./data/prefixes.json', 'w') as pref:
        json.dump(prefixes, pref, indent = 4)

"""
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    if message.content.startswith("$dex"):
        if message.content.startswith("$dex inspire"):
            await message.channel.send("\nReplying to: \"" + message.content + "\" -" + message.author.mention + "\n\n")
            await message.channel.send("\n" + get_quote())
        else:
            await message.channel.send("\nReplying to: \"" + message.content + "\" -" + message.author.mention + "\n\n")
            await message.channel.send('\nHello, this is dex at your service!')
            await client.get_channel(int(os.environ['HISTORY_CHANNEL_ID'])).send("\nMessage:\n" + message.content + "\n\nAuthor: " + str(message.author) + " | ID: " + str(message.author.id) + "\nServer: " + str(message.guild)  + "\nChannel: " + str(message.channel) + "\n")
"""

client.run(os.getenv('BOT_TOKEN'))