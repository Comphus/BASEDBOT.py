from discord.ext import commands
import discord
import asyncio
import json
import datetime
import random
import importlib
import sys
bot = commands.Bot(command_prefix='!',description="I am a bot created by Comphus mainly for the Dragon Nest Community Discord server, but I have many other functions!")

startup_ext = [
	"botmodules.BASEDBOTgames",
	"botmodules.BASEDBOTbns",
	"botmodules.BASEDBOTow",
	"botmodules.BASEDBOTdn",
	"botmodules.BASEDBOTetc",
	"botmodules.BASEDBOTmusic",
	"botmodules.BASEDBOTdiscord"
]

with open("C:/discordlogin.json") as j:
	dLogin = json.load(j)

def is_owner(ctx):
	return ctx.message.author.id == '90886475373109248'

@bot.event
async def on_command_error(error, ctx):
	if isinstance(error, commands.NoPrivateMessage):
		await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
	elif isinstance(error, commands.DisabledCommand):
		await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
	#else:
	#	print(error)

@bot.command()
@commands.check(is_owner)
async def reload(extension_name : str):
	try:
		bot.unload_extension(extension_name)
		bot.load_extension(extension_name)
		await bot.say('module {} reloaded'.format(extension_name))
	except Exception as e:
		await bot.say('reloading failed, error is:```\n{}```'.format(e))

@bot.event
async def on_message(message):
	if bot.user == message.author or message.channel.id == '168949939118800896' or message.author.id in '128044950024617984':
		return

	await bot.process_commands(message)

@bot.async_event
def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	yield from bot.change_presence(game=discord.Game(name='you like a fiddle'))
	if not hasattr(bot, 'uptime'):
		bot.uptime = datetime.datetime.now()

for extension in startup_ext:
	try:
		bot.load_extension(extension)
	except Exception as e:
		print('Failed to load extension {}\n{}'.format(extension, e))

bot.run(dLogin['username'])
