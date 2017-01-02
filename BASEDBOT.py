import discord
from cogs.utils import checks
from discord.ext import commands
import asyncio
import json
import datetime
import random
import traceback
import sys

bot = commands.Bot(command_prefix='!',description="I am a bot created by Comphus mainly for the Dragon Nest Community Discord server, but I have many other functions!")

startup_ext = [
	"cogs.BASEDBOTgames",
	"cogs.BASEDBOTbns",
	"cogs.BASEDBOTow",
	"cogs.BASEDBOTdn",
	"cogs.BASEDBOTetc",
	"cogs.BASEDBOTmusic",
	"cogs.BASEDBOTdiscord"
]

with open("C:/discordlogin.json") as j:
	dLogin = json.load(j)

@bot.event
async def on_command_error(error, ctx):
	if isinstance(error, commands.NoPrivateMessage):
		await bot.send_message(ctx.message.author, 'This command cannot be used in private messages.')
	elif isinstance(error, commands.DisabledCommand):
		await bot.send_message(ctx.message.author, 'Sorry. This command is disabled and cannot be used.')
	elif isinstance(error, commands.CommandInvokeError):
		print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
		traceback.print_tb(error.original.__traceback__)
		print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

@bot.command(hidden=True)
@checks.is_owner()
async def reload(extension_name : str):
	try:
		bot.unload_extension(extension_name)
		bot.load_extension(extension_name)
		await bot.say('module {} reloaded'.format(extension_name))
	except Exception as e:
		await bot.say('reloading failed, error is:```\n{}: {}```'.format(type(e).__name__, e))

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
