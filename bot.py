import os
import http.client
import random

import discord
from dotenv import load_dotenv

## Saved secret data to other file in directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
APEX_KEY = os.getenv('APEX_KEY')

## Permissions of the bot, diff from actual bot permissions
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

## Have the bot do something
@client.event
## When the connection is established
async def on_ready():
    print("Sanctuary Bot is ready...")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        # Simple reply
        if message.content.lower() == 'hello':
            await message.reply(f"Hello, {message.author}")
        # if the message starts with '%'
        elif message.content.lower()[0] == '%':
            command = message.content.split('%')[1]
            command_args = command.split(' ')
            # gaypex command
            if (command_args[0].lower() == 'gaypex'):
                await gaypex(command_args, message.channel)
            #coinflip command
            if (command_args[0].lower() == 'coinflip'):
                await coinflip(message)
            
# Request for apex tracker. API still needs approval
async def gaypex(command, message):
    await message.reply(f'{command}')
    conn = http.client.HTTPSConnection('https://public-api.tracker.gg/apex/v1/standard/profile/5/', 443)
    conn.request('GET', '/', headers={'TRN-Api-Key':APEX_KEY,
                                      'Accept': 'application/vnd.api+json'})
    r = conn.getresponse()
    print(r.read())
    
# Coinflip using random library
async def coinflip(message):
    side = random.choice(['Heads', 'Tails'])
    await message.reply(f"It's {side}!")
    
client.run(TOKEN)
    