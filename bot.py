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
client = discord.Client(intents=intents)

## Have the bot do something
@client.event
## When the connection is established
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    print([member.name for member in guild.members])

client.run(TOKEN)