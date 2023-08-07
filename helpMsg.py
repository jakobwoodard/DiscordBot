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