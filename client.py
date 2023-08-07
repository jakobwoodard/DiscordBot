import os

from dotenv import load_dotenv

import discord
# Saved secret data to other file in directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Worse Apex API, being used for map pool while waiting for perms
# https://apexlegendsstatus.com/
APEX_KEY = os.getenv('APEXSTATUS_KEY')

# Permissions of the bot, diff from actual bot permissions
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)