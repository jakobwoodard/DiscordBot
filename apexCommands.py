import requests

from client import APEX_KEY


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
        url=('https://lil2-gateway.apexlegendsstatus.com/gateway.php?qt=map'),
        headers=headers
    )
    # Make the response json
    resp_json = response.json()
    # Format the response
    current_map = {'map': resp_json["rotation"]["battle_royale"]["current"]["map"],
        'time': resp_json["rotation"]["battle_royale"]["current"]["remainingTimer"]}
    next_map = {'map': resp_json["rotation"]["battle_royale"]["next"]["map"],
        'time': resp_json["rotation"]["battle_royale"]["next"]["DurationInMinutes"]}
    ranked_map = {'map': resp_json["rotation"]["ranked"]["current"]["map"]
    }
    # Bot responds
    await message.reply(f"{current_map['map']} has {current_map['time']} remaining.\nThe next map will be {next_map['map']} for {next_map['time']} minutes.\nThe Ranked map is {ranked_map['map']}")
