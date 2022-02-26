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

    developer_settings_menu : stores the developer settings menu;

"""

client = discord.Client()

def get_quote():
    response = requests.get("https://zenquotes.io/api//random")
    quote_json = json.loads(response.text)
    quote = "\"" + quote_json[0]['q'] + "\" says " + quote_json[0]['a']
    return (quote)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.get_channel(int(os.environ['CONSOLE_CHANNEL_ID'])).send(".\nLogged in!\nOnline Now!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command_key = "$dex"
    if "command_key" in db.keys():
        command_key = db["command_key"]
    developer_settings_menu = "Developer Settings:\n\t\"" + command_key + "devsets 0\": Change the command key that the bot responds to.\n\t\tCurrent command key: \"" + command_key + "\"\n"
    if message.content.startswith(command_key):
        if message.content == (command_key + " devsets 0") or message.content == (command_key + " devsets 0 "):
            await message.channel.send(".\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send(".\nResend after appending the new command key!")
        elif message.content.startswith(command_key + " devsets 0 "):
            await message.channel.send(".\nOriginal message sent: \"" + message.content + "\"\n\n")
            db["command_key"] = message.content.split(command_key + " devsets 0 ",1)[1]
            command_key = db["command_key"]
            await message.channel.send(".\nCommand Key changed successfully!\nNew Command Key: " + command_key)
            await client.get_channel(int(os.environ['CONSOLE_CHANNEL_ID'])).send("\n\nCommand Key changed successfully!\nNew Command Key: " + command_key + "\n\n")
        elif message.content.startswith(command_key + " devsets"):
            await message.channel.send(".\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send(".\n" + developer_settings_menu)
        elif message.content.startswith(command_key + " inspire"):
            await message.channel.send(".\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send(".\n" + get_quote())
        else:
            await message.channel.send(".\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send('.\nHello, this is dex at your service!')


client.run(os.getenv('BOT_TOKEN'))
