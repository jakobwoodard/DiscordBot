import os

import discord
from dotenv import load_dotenv

## Saved secret data to other file in directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

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
client.run(TOKEN)
    