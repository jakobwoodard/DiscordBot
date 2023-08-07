# Guessing random number game
import random
from client import client

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
        
# Coinflip using random library
async def coinflip(message):
    side = random.choice(['Heads', 'Tails'])
    await message.reply(f"It's {side}!")