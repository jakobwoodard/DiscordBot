import os
import random
import requests
import asyncio
import time


import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import discord
from bs4 import BeautifulSoup
from dotenv import load_dotenv


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


# Have the bot do something
@client.event
# When the connection is established
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
            if (command_args[0].lower() == 'golfmoose'):
                await golfmoose(message, command_args)
            if (command_args[0].lower() == 'random'):
                await randomGuess(message)
            if (command_args[0].lower() == 'help'):
                await help(message)
                
                
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
        url=(base + 'maprotation?' + auth),
        headers=headers
    )
    # Make the response json
    resp_json = response.json()
    # Format the response
    current_map = {'map': resp_json['current']['map'],
        'time': resp_json['current']['remainingTimer']}
    next_map = {'map': resp_json['next']['map'],
        'time': resp_json['next']['DurationInMinutes']}
    # Bot responds
    await message.reply(f"{current_map['map']} has {current_map['time']} remaining.\nThe next map will be {next_map['map']} for {next_map['time']} minutes.\n")

# Help menu
# Lists all commands


async def help(message):
    await message.reply(f"`%help` - Get a list of all commands." + "\n" +
                        "`%apex map` - Get the current map in rotation" + "\n" +
                        "`%coinflip` - Flip a coin" + "\n" +
                        "`%golfmoose [region]` - Get current golfmoose deals for specified region. Currently, only NC regions are supported." + "\n" +
                        "`%random` - Play a guessing game between 0-100")


# Coinflip using random library
async def coinflip(message):
    side = random.choice(['Heads', 'Tails'])
    await message.reply(f"It's {side}!")

# Checks current golf moose deals based on specified region
### Practice for web scraping/parsing raw html output ###


async def golfmoose(message, command):
    region = command[1].lower()
    # Selenium/Pandas Chrome Web Driver initialization
    # start by defining the options
    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')
    options.add_argument('--headless') # it's more scalable to work in headless mode
    options.page_load_strategy = 'none'

    # this returns the path web driver downloaded
    chrome_path = ChromeDriverManager().install()
    chrome_service = Service(chrome_path)
    # pass the defined options and service objects to initialize the web driver
    driver = Chrome(options=options, service=chrome_service)
    driver.implicitly_wait(5)

    url = ('https://golfmoose.com/product-category/north-carolina/' + region)
    
    driver.get(url)
    time.sleep(4)

    def get_panel():
        response = ''
        deals = driver.find_elements(By.CSS_SELECTOR, "div[class*='deal-single panel']")
        deals_dict = {}
        for deal in deals:
            # find deal/prices
            title = deal.find_element(By.CLASS_NAME, "deal-title").text # title
            #desc = deal.find_element(By.CLASS_NAME, "text-muted").text # Deal
            prices = deal.find_elements(By.CSS_SELECTOR, "span[class*='woocommerce-Price-amount amount']")
            prev_price = prices[0].find_element(By.TAG_NAME, "bdi").text
            new_price = prices[1].find_element(By.TAG_NAME, "bdi").text
            deal_dict = {
                'title': title,
                #'desc': desc,
                'prev_price': prev_price,
                'new_price': new_price
            }
            deals_dict[title] = deal_dict
            
        for key in deals_dict.keys():
            formatted_deal = f"{deals_dict[key]['title']}   ({deals_dict[key]['new_price']}) \n"
            response += formatted_deal
            
        return response
    
    bot_response = get_panel()
    print(bot_response)
    await message.reply(bot_response)
    


# Guessing random number game
async def randomGuess(message):
    await message.reply(f"Guess a number between 0 and 100")
    randomNum = random.randint(0, 100)
    remain = 5
    print(randomNum)

    i = 0
    while i != 5:
        msg = await client.wait_for('message')
        try:
            guess = int(msg.content)
        except ValueError:
            await msg.reply("Invalid number, try again")
            continue
        if (guess == randomNum):
            await msg.reply(f"Correct!")
            break
        elif (guess > randomNum and remain > 1):
            remain = remain - 1
            await msg.reply(f"Try a lower number, " + str(remain) + " guesses left")
        elif (guess < randomNum and remain > 1):
            remain = remain - 1
            await msg.reply(f"Try a higher number, " + str(remain) + " guesses left")
        else:
            remain = remain - 1
            await msg.reply(f"Please enter a number between 0 and 100, " + str(remain) + " guesses left")
        i = i + 1
    else:
        await msg.reply(f"Sorry, the number was " + str(randomNum) + "!")


client.run(TOKEN)
