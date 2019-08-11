# -*- coding: utf-8 -*-
"""
BASEDBOT is a Discordapp chat bot written in python using the Discord.py library and the discord.py commands extension
discord.py library: https://github.com/Rapptz/discord.py

Mainly written for the DNCD server, and has been rewritten and expanded over the years to accomidate use on multiple servers.
This is essentially a jack of all trades chat bot that can do a multitude of tasks.
ctx is used the invocation context when calling a command
BASEDBOT.py is a modified version of basic_bot.py (https://github.com/Rapptz/discord.py/blob/master/examples/basic_bot.py)
"""
import discord
from cogs.utils import checks
from discord.ext import commands
import asyncio
import aiohttp
import logging
from bs4 import BeautifulSoup
import json
import datetime
import random
import traceback
import sys
import re


bot = commands.AutoShardedBot(shard_count=2, command_prefix='!',description="I am a bot created by Comphus mainly for the Dragon Nest Community Discord server, but I have many other functions!")
logger = logging.getLogger('discord')

startup_ext = [
	"cogs.games",
	"cogs.bns",
	"cogs.ow",
	"cogs.dn",
	"cogs.etc",	
	"cogs.music",
	"cogs.discord",
	"cogs.backgrounds"
]

with open("C:/discordlogin.json") as j:
	dLogin = json.load(j)

@bot.event
async def on_command_error(ctx, error):
	try:
		if ctx.message.guild.id == 110373943822540800:
			return
	except:
		pass
	if isinstance(error, commands.NoPrivateMessage):
		await ctx.message.author.send('This command cannot be used in private messages.')
	elif isinstance(error, commands.DisabledCommand):
		await ctx.message.author.send('Sorry. This command is disabled and cannot be used.')
	elif isinstance(error, commands.CommandInvokeError):
		if "Missing Permissions" in str(error.original):
			try:
				await ctx.message.author.send('BASEDBOT does not have the required permissions to execute `!{}`.'.format(ctx.command.qualified_name))
			except:
				pass
		else:
			print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
			traceback.print_tb(error.original.__traceback__)
			print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)

@bot.command(hidden=True)
@checks.is_owner()
async def reload(ctx, extension_name : str = None):
	if extension_name is None:
		for i in startup_ext:
			try:
				bot.reload_extension(i)
			except Exception as e:
				await ctx.send('{} cog reloading failed, error is:```\n{}: {}```'.format(i,type(e).__name__, e))
		await ctx.send("Extensions reloaded")
		return
	try:
		bot.reload_extension(extension_name)
		await ctx.send('module {} reloaded'.format(extension_name))
	except Exception as e:
		await ctx.send('reloading failed, error is:```\n{}: {}```'.format(type(e).__name__, e))

@bot.event
async def on_message(message):
	if bot.user == message.author or message.channel.id == 168949939118800896 or message.author.id == 128044950024617984:
		return
	await bot.process_commands(message)

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	await bot.change_presence(activity=discord.Activity(name='you like a fiddle'))
	if not hasattr(bot, 'uptime'):
		bot.uptime = datetime.datetime.now()

for extension in startup_ext:
	try:
		bot.load_extension(extension)
	except Exception as e:
		print('Failed to load extension {}\n{}'.format(extension, e))

bot.run(dLogin['username'])