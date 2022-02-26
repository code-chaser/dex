import discord
import os
import requests
import json
from replit import db

"""

VARIABLES
    
    command_key : stores the string for the bot to acknowldge
        every message that starts with that string;

    client : stores the bot's client address;

"""

client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api//random")
    quote_json = json.loads(response.text)
    quote = "\"" + quote_json[0]['q'] + "\" -" + quote_json[0]['a']
    return (quote)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.get_channel(int(os.environ['CONSOLE_CHANNEL_ID'])).send(".\nLogged in!\nOnline Now!")
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = db["command_key"]))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    
    if message.content.startswith("$dex"):
        if message.content.startswith("$dex inspire"):
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send("\n" + get_quote())
        else:
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send('\nHello, this is dex at your service!')


client.run(os.getenv('BOT_TOKEN'))
