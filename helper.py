import json

from discord.ext import commands


with open("./config/config.json") as cfg:
	config = json.load(cfg)

owner = config["owner"]

def is_owner():
	return commands.check(lambda ctx: ctx.message.author.id == owner)