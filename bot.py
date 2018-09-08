import discord
import json
import re
import asyncio
from markov import *

from time import sleep
from discord.ext import commands

# set config variables
with open("./config/config.json") as cfg:
    config = json.load(cfg)

token = config["token"]

bot = commands.Bot(command_prefix='.')

# make sure the message is clean of links, special chars, etc
def sanitize(msg):
    # remove links
    msg = re.sub(r'https?:\/\/.*', '', msg)
    # remove emojis and mentions
    msg = re.sub(r'<.*>', '', msg)
    # remove special characters
    msg = re.sub('[^A-Za-z0-9 \/\',.]+', '', msg)
    # remove whitespace
    msg = msg.strip()

    return msg

async def random_message_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        channel = bot.get_channel(461634259212435468)
        await type_message(channel)

        def check(m):
            return m.channel == channel

        while True:
            try:
                await bot.wait_for('message', check = check, timeout=10)
            except asyncio.TimeoutError:
                break
            
            await type_message(channel)

        await asyncio.sleep(random.randint(900, 1800))

async def type_message(channel):
    sleep(2)
    async with channel.typing():
        message = do_markov("./config/history.txt")
        sleep(random.randint(4,6))

    await channel.send(message)

def is_command(message):
    prefixes = ['.', '/', '!', '$']
    for symbol in prefixes:
        if message.startswith(symbol):
            return True
    return False

# log in status
@bot.event
async def on_ready():
    bot.owner_id = 137723737922338816
    print('Logged in as') 
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):  
    await bot.process_commands(message)

    if "<@"+str(bot.user.id)+">" in message.content:
        channel = message.channel
        type_message(channel)

    if message.author.id == bot.owner_id and not is_command(message.content):
       msg = sanitize(message.content) 
       with open("./config/history.txt", "a") as _file:
            _file.write(msg + "\n")            


@bot.command()
async def markov(ctx):
    await type_message(ctx.channel)

@bot.command()
async def load(ctx):
    if ctx.message.author.id == bot.owner_id:
        channels = bot.get_all_channels()
        for channel in channels:
            if not (channel.name == "spam"):
                async for msg in channel.history(limit=None, reverse=True):
                    if msg.author.id == bot.owner_id and not is_command(msg.content):
                        message = sanitize(msg.content)
                        # print(message)
                        with open("./config/history.txt", "a") as _file:
                            _file.write(message + "\n")

        await ctx.send("Loading complete.")
    else:
        await ctx.send("Access denied.")

@bot.command()
async def q(ctx):
    if ctx.message.author.id == bot.owner_id:
        await bot.logout()
    else:
        await ctx.send("Access denied.")
                   
bot.loop.create_task(random_message_loop())
bot.run(token)