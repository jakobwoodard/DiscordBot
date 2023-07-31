import os
import http.client

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
        if message.content.lower() == 'hello':
            await message.reply(f"Hello, {message.author}")
        elif message.content.lower()[0] == '%':
            await message.reply(f'Executing command {message.content.split("%")[1]}')
            await gaypex(message.content.split("%")[1], message.channel)
            
async def gaypex(command, channel):
    await channel.send(f'{command}')
    conn = http.client.HTTPSConnection('https://public-api.tracker.gg/apex/v1/standard/profile/5/', 443)
    conn.request('GET', '/', headers={'TRN-Api-Key':APEX_KEY,
                                      'Accept': 'application/vnd.api+json'})
    r = conn.getresponse()
    print(r.read())
    
client.run(TOKEN)
    