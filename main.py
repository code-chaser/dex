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
    await client.change_presence(activity=discord.Game("listening to " + db["command_key"]))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command_key = "$dex"
    devsets_key = "devsets"
    if "command_key" in db.keys():
        command_key = db["command_key"]
    if "devsets_key" in db.keys():
        devsets_key = db["devsets_key"]
    developer_settings_menu = "Developer Settings:\n-\t\"" + command_key + " " + devsets_key + " 0\": Change the command key that the bot responds to.\n\t\tCurrently it's: \"" + command_key + "\"\n-\t\"" + command_key + " " + devsets_key + " 1\": Change the command to enter developer settings.\n\t\tCurrently it's: \"" + devsets_key + "\"\n"
    if message.content.startswith(command_key):
        if message.content == (command_key + " " + devsets_key + " 0") or message.content == (command_key + " " + devsets_key + " 0 "):
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send("\nResend after appending the new command!")
        elif message.content.startswith(command_key + " " + devsets_key + " 0 "):
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            db["command_key"] = message.content.split(command_key + " " + devsets_key + " 0 ",1)[1]
            command_key = db["command_key"]
            await message.channel.send("\nCommand changed successfully!\nNew Command: " + command_key)
            await client.get_channel(int(os.environ['CONSOLE_CHANNEL_ID'])).send("\n\nCommand changed successfully!\nNew Command: " + command_key + "\n\n")
        elif message.content.startswith(command_key + " " + devsets_key + " 1 "):
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            db["devsets_key"] = message.content.split(command_key + " " + devsets_key + " 1 ",1)[1]
            devsets_key = db["devsets_key"]
            await message.channel.send("\nCommand changed successfully!\nNew Command: " + devsets_key)
            await client.get_channel(int(os.environ['CONSOLE_CHANNEL_ID'])).send("\n\nCommand changed successfully!\nNew Command: " + devsets_key + "\n\n")
        elif message.content == (command_key + " " + devsets_key + " 1") or message.content == (command_key + " " + devsets_key + " 1 "):
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send("\nResend after appending the new command!")
        elif message.content.startswith(command_key + " " + devsets_key):
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send("\n" + developer_settings_menu)
        elif message.content.startswith(command_key + " inspire"):
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send("\n" + get_quote())
        else:
            await message.channel.send("\nOriginal message sent: \"" + message.content + "\"\n\n")
            await message.channel.send('\nHello, this is dex at your service!')


client.run(os.getenv('BOT_TOKEN'))
