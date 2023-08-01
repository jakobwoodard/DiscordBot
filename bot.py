import os
import random
import requests

import discord
from dotenv import load_dotenv

## Saved secret data to other file in directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

## Worse Apex API, being used for map pool while waiting for perms
## https://apexlegendsstatus.com/
APEX_KEY = os.getenv('APEXSTATUS_KEY')

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

### What the bot does when a message is sent.... it's always watching ###
@client.event
async def on_message(message):
    # Bot can't respond to itself #
    if message.author == client.user:
        return
    else:
        # Simple reply
        if message.content.lower() == 'hello':
            await message.reply(f"Hello, {message.author}")
            
            
        ### Start of command readings ###
        ### Can have multiple command prompts i.e. not just '%' ###
        ### But may interfere with existing bots in server ###
        elif message.content.lower()[0] == '%':
            command = message.content.split('%')[1]
            command_args = command.split(' ')
            ## Prompt for all apex commands ##
            ## '%apex [arg1] [arg2]...' ##
            if (command_args[0].lower() == 'apex'):
                await apex(command_args, message)
            ## Prompt for coinflip ##
            ## '%coinflip' ##
            if (command_args[0].lower() == 'coinflip'):
                await coinflip(message)
            
### Request for apex tracker. API still needs approval, so using worse api ###
### '%apex [arg1] [arg2] [arg3]... ' ###
### '%apex map' gives the current and next map ###
async def apex(command, message):
    auth = f'auth={APEX_KEY}'
    base = f'https://api.mozambiquehe.re/'
    
    ## Filter the command. Since only 1 valid commant atm (map), all others are considered invalid ##
    if command[1].lower() != 'map':
        await message.reply("Invalid command. Expected: '\%apex map'")
        return
    
    # Build headers for requests.get()
    headers = {
        'Authorization': APEX_KEY
    # Save the response
    }
    response = requests.get(
        url= (base + 'maprotation?' + auth),
        headers=headers
    )
    # Make the response json
    resp_json = response.json()
    # Format the response
    current_map = {'map':resp_json['current']['map'], 'time':resp_json['current']['remainingTimer']}
    next_map = {'map':resp_json['next']['map'], 'time':resp_json['next']['DurationInMinutes']}
    # Bot responds
    await message.reply(f"{current_map['map']} has {current_map['time']} remaining.\nThe next map will be {next_map['map']} for {next_map['time']} minutes.\n")
    
    
# Coinflip using random library
async def coinflip(message):
    side = random.choice(['Heads', 'Tails'])
    await message.reply(f"It's {side}!")
    
client.run(TOKEN)
    