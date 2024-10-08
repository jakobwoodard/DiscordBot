import os
import random
import requests
import time

import asyncio
import discord
from discord import FFmpegPCMAudio
from bs4 import BeautifulSoup
from dotenv import load_dotenv


## Saved secret data to other file in directory
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

# ## Worse Apex API, being used for map pool while waiting for perms
# ## https://apexlegendsstatus.com/
# APEX_KEY = os.getenv("APEXSTATUS_KEY")

## Permissions of the bot, diff from actual bot permissions
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)
timeout_id = 1217540405097402429


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
        if message.content.lower() == "hello":
            await message.reply(f"Hello, {message.author}")

        ### Start of command readings ###
        ### Can have multiple command prompts i.e. not just '%' ###
        ### But may interfere with existing bots in server ###
        elif message.content.lower()[0] == "%":
            command = message.content.split("%")[1]
            command_args = command.split(" ")
            ## Prompt for all apex commands ##
            ## '%apex [arg1] [arg2]...' ##
            if command_args[0].lower() == "apex":
                await apex(command_args, message)
            ## Prompt for coinflip ##
            ## '%coinflip' ##
            if command_args[0].lower() == "coinflip":
                await coinflip(message)
            if command_args[0].lower() == "golfmoose":
                await golfmoose(message, command_args)
            if command_args[0].lower() == "timeout":
                await timeout(message, command_args)


### Request for apex tracker. API still needs approval, so using worse api ###
### '%apex [arg1] [arg2] [arg3]... ' ###
### '%apex map' gives the current and next map ###
async def apex(command, message):
    await message.reply("This command is no longer supported.")
    # auth = f"auth={APEX_KEY}"
    # base = f"https://api.mozambiquehe.re/"

    # ## Filter the command. Since only 1 valid commant atm (map), all others are considered invalid ##
    # if command[1].lower() != "map":
    #     await message.reply("Invalid command. Expected: '\%apex map'")
    #     return

    # # Build headers for requests.get()
    # headers = {
    #     "Authorization": APEX_KEY
    #     # Save the response
    # }
    # response = requests.get(url=(base + "maprotation?" + auth), headers=headers)
    # # Make the response json
    # resp_json = response.json()
    # # Format the response
    # current_map = {
    #     "map": resp_json["current"]["map"],
    #     "time": resp_json["current"]["remainingTimer"],
    # }
    # next_map = {
    #     "map": resp_json["next"]["map"],
    #     "time": resp_json["next"]["DurationInMinutes"],
    # }
    # # Bot responds
    # await message.reply(
    #     f"{current_map['map']} has {current_map['time']} remaining.\nThe next map will be {next_map['map']} for {next_map['time']} minutes.\n"
    # )


# Coinflip using random library
async def coinflip(message):
    side = random.choice(["Heads", "Tails"])
    await message.reply(f"It's {side}!")


# Checks current golf moose deals based on specified region
### Practice for web scraping/parsing raw html output ###
async def golfmoose(message, command):
    region = command[1].lower()
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    }
    ## Gets the entire page's raw html to be parsed ##
    response = requests.get(
        url=("https://golfmoose.com/product-category/north-carolina/" + region),
        headers=headers,
    )
    print(response.text)


# Fetches timed out user's soul, sending them to the shadow realm (t/o channel)
# Where they are stuck for the given time limit (defualt 15s)
async def timeout(message, command):
    # check valid formatting
    if len(command) == 1:
        await message.channel.send(
            "Invalid format. Expected '%timeout [user] [time] "
            + str(message.author.display_name)
        )
    else:
        # join the channel and fetch their souls ;)
        voice_channel = message.author
        channel = None
        if voice_channel != None:
            channel = message.author.voice.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio("souls.mp3")
            player = voice.play(source)
            await timeout_helper(2.5, message, command, player)
        # fail if user's not in a channel
        else:
            await message.channel.send("User is not in a channel")


# helper function for timeout, handles role manipulation and timing for audio
async def timeout_helper(sleep, message, command, player):
    await asyncio.sleep(sleep)
    player.disconnect()
    timeout_channel = client.get_channel(timeout_id)
    victim = command[1].lower()
    # search the server for the given display name
    for member in client.guilds[0].members:
        # we have found the mentioned user
        if member.display_name.lower() == victim:
            # id of the timeout role (can't access anything)
            timeout_role = None
            for role in client.guilds[0].roles:
                if role.name.lower() == "timeout":
                    timeout_role = role
                    # remember the user's current role(s)
                    cur_roles = []

                    for role in member.roles:
                        if role.name != "@everyone":
                            cur_roles.append(role)
                    print(cur_roles)

                    # remove the user's current role(s)
                    await member.remove_roles(*cur_roles)
                    # give the user the timeout role
                    await member.add_roles(timeout_role)
                    # move the user to the timeout corner
                    await member.move_to(timeout_channel)
                    # wait the timeout period
                    if len(command) == 3:
                        time.sleep(int(command[2]))
                    else:
                        time.sleep(15)
                    # reset user perms
                    await member.remove_roles(timeout_role)
                    await member.add_roles(*cur_roles)


client.run(TOKEN)
