import os
import random
import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import discord
import youtube_dl
import asyncio
from dotenv import load_dotenv


# Saved secret data to other file in directory
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Worse Apex API, being used for map pool while waiting for perms
# https://apexlegendsstatus.com/
APEX_KEY = os.getenv('APEXSTATUS_KEY')

# Permissions of the bot, diff from actual bot permissions
intents = discord.Intents.all()
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
            if (command_args[0].lower() == 'music'):
                await music(message, command_args)
            if (command_args[0].lower() == 'help'):
                await help(message)
                
                
### Help menu ###
### Lists all commands ###
async def help(message):
    await message.reply(f"`%help` - Get a list of all commands." + "\n" +
                        "`%apex map` - Get the current map in rotation" + "\n" +
                        "`%coinflip` - Flip a coin" + "\n" +
                        "`%golfmoose [state] [region]` - Get current golfmoose deals for specified region." + "\n" +
                        "`%golfmoose states` for all supported states" + "\n" + 
                        "`%golfmoose [state] regions` for all supported regions for the given state." + "\n" +
                        "`%random` - Play a guessing game between 0-100")
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


# Coinflip using random library
async def coinflip(message):
    side = random.choice(['Heads', 'Tails'])
    await message.reply(f"It's {side}!")

# Checks current golf moose deals based on specified region
### Practice for web scraping/parsing raw html output ###

### Checks golf moose for deals in the specified state/region ###
### command_args in form 'golfmoose, [state], [region]' ###
async def golfmoose(message, command_args):
    working_msg = await message.reply("Working...")
    
    states = ['Arizona', 'Northern-California', 'Southern-California', 'Carolinas', 'Florida', 'Georgia', 'Illinois', 'Nevada', 'Oregon', 'Texas', 'Virginia', 'Washington', 'Wisconsin', 'Worldwide']
    regions = {'arizona': ['Phoenix', 'Prescott', 'Sedona', 'Tucson'],
               'northern-california': ['Central-Coast', 'East-Bay', 'Fresno', 'Lake-Tahoe', 'Monterey', 'North-Bay', 'North-State', 'Sacramento', 'San-Jose', 'Santa-Cruz', 'Sierra-Foothills', 'Stockton'],
               'southern-California': ['Coast', 'Inland-Empire', 'Los-Angeles', 'Mojave', 'Palm-Springs', 'San-Diego', 'Santa-Barbara', 'Temecula'],
               'carolinas':['Augusta', 'Coastal', 'Fayetteville', 'Greenville', 'Greenville-South-Carolina', 'Greensboro', 'Hilton-Head', 'Mountains', 'Myrtle-Beach', 'Pinehurst', 'Raleigh'],
               'florida': ['Central', 'Central-East', 'Lakeland', 'Northeast-Florida', 'Orlando', 'Southeast', 'Southwest-Florida', 'Tampa'],
               'georgia': ['Atlanta', 'Augusta-Georgia', 'Savannah'],
               'illinois': ['Chicago-Northwest', 'Chicago-South', 'Chicago-Southwest', 'Chicago-West', 'Rockford', 'Southern-Illinois'],
               'nevada': ['Las-Vegas', 'Reno', 'Mojave'],
               'oregon': ['Bend', 'Eugene', 'Northeasten-Oregon', 'Portland', 'Southern-Oregon'],
               'texas': ['Austin', 'Dallas-Fort-Worth', 'Hill-Country', 'San-Antonio'],
               'virginia':['Hampton-Roads'],
               'wisconsin': ['Central-Wisconsin', 'North', 'South', 'West'],
               'worldwide':['Mexico']}
    
    if len(command_args) == 2 and command_args[1].lower() == 'states':
        # list all available states
        response = 'Supported States: \n'
        for state in states:
            formatted_list = f"{state} \n"
            response += formatted_list
        await message.reply(response)
        await working_msg.delete()
        return
    
    elif len(command_args) == 2 and command_args[1].lower() == 'washington':
        await webscrape(message, command_args[1], None)
        await working_msg.delete()
        
    elif len(command_args) == 3 and command_args[1].lower() in (state.lower() for state in states) and command_args[2].lower() == 'regions':
        # list all available regions in the specified state
        response = f"Supported Regions for {command_args[1].upper()}: \n"
        for region in regions[command_args[1].lower()]:
            formatted_list = f"{region} \n"
            response += formatted_list
        await message.reply(response)
        await working_msg.delete()
        return

    elif len(command_args) == 3 and command_args[1].lower() in (state.lower() for state in states) and command_args[2].lower() in (region.lower() for region in regions[command_args[1]]):
        # run the meat and potatoes
        await webscrape(message, command_args[1], command_args[2])
        await working_msg.delete()
        
    else:
        await message.reply("Invalid command syntax. Available commands: \n '%golfmoose [state] [region]' \n '%golfmoose states' \n '%golfmoose [state] regions'")
        await working_msg.delete()
        return

    
async def webscrape(message, state, region):
    
    def get_panel():
        response = ''
        deals = driver.find_elements(
            By.CSS_SELECTOR, "div[class*='deal-single panel']")
        deals_dict = {}
        for deal in deals:
            # find deal/prices
            title = deal.find_element(
                By.CLASS_NAME, "deal-title").text  # title
            # desc = deal.find_element(By.CLASS_NAME, "text-muted").text # Deal
            prices = deal.find_elements(
                By.CSS_SELECTOR, "span[class*='woocommerce-Price-amount amount']")
            prev_price = prices[0].find_element(By.TAG_NAME, "bdi").text
            new_price = prices[1].find_element(By.TAG_NAME, "bdi").text
            deal_dict = {
                'title': title,
                # 'desc': desc,
                'prev_price': prev_price,
                'new_price': new_price
            }
            deals_dict[title] = deal_dict

        for key in deals_dict.keys():
            formatted_deal = f"{deals_dict[key]['title']}   ({deals_dict[key]['new_price']}) \n"
            response += formatted_deal

        return response
    
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
    
    # Washington special case
    if state.lower() == 'washington':
        url = ('https://golfmoose.com/product-category/' + state)
    # Carolinas special case
    elif state.lower() == 'carolinas':
        url = ('https://golfmoose.com/product-category/north-carolina/' + region)
    # Base case
    else:
        url = ('https://golfmoose.com/product-category/' + state + '/' + region)
    
    driver.get(url)
    time.sleep(4)
    
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


### Setup code from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py ###
# youtube_dl.utils.bug_reports_message = lambda: ''

# ytdl_format_options = {
#     'format': 'bestaudio/best',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }

# ffmpeg_options = {
#     'options': '-vn'
# }

# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.5):
#         super().__init__(source, volume)
#         self.data = data
#         self.title = data.get('title')
#         self.url = ""

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]
#         filename = data['title'] if stream else ytdl.prepare_filename(data)
#         return filename
# ### END MUSIC SETUP ###

# ### Music bot controls ###
# async def music(message, commands):
#     # '%music play [query]'
#     ctx = message.channel
#     if (commands[1].lower() == 'play' and len(commands) >= 3):
#         try :
#             server = ctx.message.guild
#             voice_channel = server.voice_client

#             ## Webscrape for top result from yt and play audio ##
#             async with ctx.typing():
#                 search_link = "http://www.youtube.com/results?search_query=" + '+'.join(commands[3:])
#                 search_result = requests.get(search_link).text
#                 soup = BeautifulSoup(search_result, 'html.parser')
#                 videos = soup.select(".yt-uix-tile-link")
#                 if not videos:
#                     raise KeyError("No video found")
#                 link = "https://www.youtube.com" + videos[0]["href"]
#                 filename = await YTDLSource.from_url(link)
#                 voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
#             await ctx.send('**Now playing:** {}'.format(filename))
#         except:
#             if not ctx.message.author.voice:
#                 await ctx.send("{} is not connected to a voice channel".format(message.author.name))
#                 return
#             else:
#                 channel = message.author.voice.channel
#             await channel.connect()
#             music(message, commands)
#     # '%music stop'
#     elif (commands[1].lower() == 'stop'):
#         voice_client = message.guild.voice_client
#         if voice_client.is_playing():
#             await voice_client.stop()
#         else:
#             await ctx.send("The bot is not playing anything at the moment.")
#     # '%music pause'
#     elif (commands[1].lower() == 'pause'):
#         voice_client = message.guild.voice_client
#         if voice_client.is_playing():
#             await voice_client.pause()
#         else:
#             await ctx.send("The bot is not playing anything at the moment.")
#     # '%music resume'
#     elif (commands[1].lower() == 'resume'):
#         voice_client = message.guild.voice_client
#         if voice_client.is_paused():
#             await voice_client.resume()
#         else:
#             await ctx.send("The bot was not playing anything before this. Use `%music play [query]` command")
    

client.run(TOKEN)
