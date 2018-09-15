import discord
import json
import random
import re
import asyncio
from markov import do_markov

from time import sleep
from discord.ext import commands
from helper import is_owner

# set config variables
with open("./config/config.json") as cfg:
    config = json.load(cfg)

token = config["jtoken"] 
owner = config["owner"]

bot = commands.Bot(command_prefix='.')

# make sure the message is clean of links, special chars, etc
def sanitize(message):
    # remove links
    message = re.sub(r'https?:\/\/.*', '', message)
    # remove emojis and mentions
    message = re.sub(r'<.*>', '', message)
    # remove special characters
    message = re.sub('[^A-Za-z0-9 /\',.?\"]+', '', message)
    # remove whitespace
    message = message.strip()

    if len(message) > 1:
        message = message.capitalize()
        if not message.endswith(".") or message.endswith("?"):
            message += "."

    return message

def is_command(message):
    prefixes = ['.', '/', '!', '$', '`']
    for symbol in prefixes:
        if message.startswith(symbol):
            return True
    return False

async def type_message(channel):
    await asyncio.sleep(2)
    async with channel.typing():
        message = do_markov("./config/history.txt")
        await asyncio.sleep(random.randint(4,6))

    await channel.send(message)

# log in status
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.user_id = 137723737922338816
    await bot.change_presence(activity=discord.Game("markov.exe"))

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if "<@"+str(bot.user.id)+">" in message.content:
        channel = message.channel
        await type_message(channel)

        def check(m):
            return (m.channel == channel) and ("<@"+str(bot.user.id)+">" not in m.content) and (m.author.id != bot.user.id)

        while True:
            try:
                await bot.wait_for('message', check = check, timeout=20)
            except asyncio.TimeoutError:
                break
            await type_message(channel)

    if "jake" in message.content.lower():
        channel = message.channel
        await type_message(channel)

    if isinstance(message.channel, discord.DMChannel) and (message.author.id != bot.user.id):
        await type_message(message.channel)

    if message.author.id == bot.owner_id and not is_command(message.content):
       message = sanitize(message.content)
       with open("./config/history.txt", "a") as _file:
            _file.write(message + "\n")


# generate a sentence
@bot.command()
async def markov(ctx):
    await type_message(ctx.channel)

# get all messages from server
@bot.command()
@is_owner()
async def load(ctx):
    channels = bot.get_all_channels()
    for channel in channels:
        await ctx.channel.send("Collecting messages in #"+channel.name)
        if not (channel.name == "spam"):
            async for message in channel.history(limit=None, reverse=True):
                if message.author.id == owner and not is_command(message.content):
                    message = sanitize(message.content)
                    if len(message) > 0:
                        with open("./config/history.txt", "a") as _file:
                            _file.write(message + "\n")
    await ctx.send("Loading complete.")

# log out
@bot.command()
@is_owner()
async def q(ctx):
    await bot.logout()

#bot.loop.create_task(random_message_loop())

# run
bot.run(token)