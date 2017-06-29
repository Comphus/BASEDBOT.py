from discord.ext import commands
import discord.utils

"""
stuff to check for permissions as well as to
check if it is in the DNCD and/or lounge
since this bot is mainly for the DNCD
"""
DNCDmods = []
with open('C:/DISCORD BOT/DiscordStuff/Mods.txt','r') as f:
	for i in f:
		DNCDmods.append(int(i.strip('\n')))

def is_owner():
	def predicate(ctx):
		return ctx.message.author.id == 90886475373109248
	return commands.check(predicate)

def not_lounge():
	def predicate(ctx):
		if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
			return False
		return ctx.message.channel.id != 106293726271246336
	return commands.check(predicate)

def in_dncd():
	def predicate(ctx):
		if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
			return False
		return ctx.message.guild.id == 106293726271246336
	return commands.check(predicate)

def dncd_not_lounge():
	def predicate(ctx):
		if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
			return False
		return (ctx.message.channel.id != 106293726271246336 and ctx.message.guild.id == 106293726271246336)
	return commands.check(predicate)

def is_admin():
	def predicate(ctx):
		if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
			return False
		return ctx.message.author.guild_permissions.administrator
	return commands.check(predicate)

def dncd_admin():
	def predicate(ctx):
		if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
			return False
		return (ctx.message.author.guild_permissions.administrator and ctx.message.guild.id == 106293726271246336)
	return commands.check(predicate)

def dncd_mod():
	def predicate(ctx):
		if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
			return False
		return ctx.message.author.id in DNCDmods
	return commands.check(predicate)

def dncd_mod_or_admin():
	def predicate(ctx):
		if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
			return False
		return (ctx.message.author.id in DNCDmods or ctx.message.author.guild_permissions.administrator)
	return commands.check(predicate)
