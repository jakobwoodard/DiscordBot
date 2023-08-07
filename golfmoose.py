import time

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

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
    
