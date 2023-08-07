from apexCommands import apex
from golfmoose import golfmoose
from helpMsg import help
from randomGames import randomGuess, coinflip
from musicPlayer import music


from client import client, TOKEN

# Have the bot do something
@client.event
# When the connection is established
async def on_ready():
    print("Sanctuary Bot is ready...")

### What the bot does when a message is sent.... it's always watching ###


### Interpret the command. Done this way to support mulitple types of commands. ###
### New commands should either be added to existing files or have own files created. ###
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
            if (command_args[0].lower() == 'apex'):
                await apex(command_args, message)
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

client.run(TOKEN)
