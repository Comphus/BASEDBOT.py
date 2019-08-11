# -*- coding: utf-8 -*-
"""
The discord module for BASEDBOT.
Allows the user to easily access information given by the Discord API through the commands in this file.
"""
from discord.ext import commands
import discord
from .utils import checks
import asyncio
import inspect
import io
import logging
import json
from datetime import datetime, date, timedelta
logging.basicConfig()

with open('C:/DISCORD BOT/DiscordStuff/joins.json') as f:
	joins = json.load(f)
with open('C:/DISCORD BOT/DiscordStuff/leaves.json') as f:
	leaves = json.load(f)

class bbDiscord(commands.Cog):
	"""
	discord functions for BASEDBOT
	"""
	def __init__(self, bot):
		self.bot = bot
		self.memeList = {}
		self.karaoke = [[], False]

	@commands.command(enabled=False)
	@checks.dncd_mod_or_admin()
	async def meme(self, ctx):
		message = ctx.message
		if message.channel.id not in self.memeList:
			self.memeList[message.channel.id] = True
			await ctx.send("meme mode is on!")
			return
		if self.memeList[message.channel.id] == True:
			self.memeList[message.channel.id] = False
			await ctx.send("meme mode is off!")
		else:
			self.memeList[message.channel.id] = True
			await ctx.send("meme mode is on!")

	async def memecheck(self, message):
		if self.memeList[message.channel.id] == True:
			c = len(message.content.split())
			d = 0
			for m in message.content.split():
				if m.startswith('<') and m.endswith('>') and m.count(':') == 2:
					d += 1
				else:
					try:
						print(m)
					except Exception:
						d += 1
			if d != c:
				await message.delete()

	@commands.command()
	@commands.guild_only()
	@checks.dncd_mod_or_admin()
	async def purge(self, ctx, num : int = 50):
		await ctx.message.channel.purge(limit=num)

	@commands.command(hidden=True)
	@checks.dncd_mod()
	async def logs(self, ctx, id : str = None, chan : discord.TextChannel = None):
		if id is None:
			await ctx.send("need a user id from the DNCD to pull up logs from")
		ch = ctx.message.guild.channels
		for i in ch:
			if isinstance(i, discord.TextChannel) and i.id not in (106301620500836352,106560613794197504):
				with io.open('C:/DISCORD BOT/message_logs/{}_Logs.txt'.format(i.name),encoding='utf-8') as f:
					if chan is not None:
						if chan == i:
							returnval = "**{}**```\n".format(i.name)
							justincase = []
							for line in f:
								if id in line:
									returnval += line.replace("@everyone", "@--everyone").replace("@here","@--here")
								if len(returnval) >=1700:
									returnval += "```"
									justincase.append(returnval)
									returnval = "```\n"
							returnval += "```"
							if len(justincase) > 0:
								if returnval != "**{}**```\n".format(i.name):
									justincase.append(returnval)
								for i in justincase:
									await ctx.send(i)
							else:
								if returnval != "**{}**```\n```".format(i.name):
									await ctx.send(returnval)
					else:
						returnval = "**{}**```\n".format(i.name)
						justincase = []
						for line in f:
							if id in line:
								returnval += line.replace("@everyone", "@--everyone").replace("@here","@--here")
							if len(returnval) >=1700:
								returnval += "```"
								justincase.append(returnval)
								returnval = "```\n"
						returnval += "```"
						if len(justincase) > 0:
							if returnval != "**{}**```\n".format(i.name):
								justincase.append(returnval)
							for i in justincase:
								await ctx.send(i)
						else:
							if returnval != "**{}**```\n```".format(i.name):
								await ctx.send(returnval)

	@commands.command()
	@commands.guild_only()
	@checks.dncd_mod_or_admin()
	async def vanish(self, ctx):
		message = ctx.message
		van = 0
		if len(message.content.split()) not in (3,2):
			await message.channel.send('The format for !vanish is: "!vanish (@mention to person(nothing if yourself)) (number of messages to delete)" and is only accessable to chatmods and above.')
			return
		if message.content.split()[-1].isdigit():
			van = int(message.content.split()[-1])
		elif message.content.split()[1].isdigit():
			van = int(message.content.split()[1])
		else:
			await message.channel.send('The format for !vanish is: "!vanish (@mention to person(nothing if yourself)) (number of messages to delete)" and is only accessable to chatmods and above.')
			return
		mem = None
		if len(message.content.split()) == 2:
			mem = message.author
		else:
			try:
				mem = message.mentions[0]
			except:
				await message.channel.send('The format for !vanish is: "!vanish (@mention to person(nothing if yourself)) (number of messages to delete)" and is only accessable to chatmods and above.')
				return
		cTime = datetime.now()
		counter = 0
		async for log in message.channel.history():
			if log.author == mem:
				await log.delete()
				counter += 1
			if counter == van:
				break
		with io.open('C:/DISCORD BOT/DiscordStuff/vanishlog.txt','a',encoding='utf-8') as f:
			s = ("{} {} Name: {} ID: {} What they wrote: {}\n".format(str(datetime.now().strftime("%m/%d/%Y %H:%M:%S")), message.guild.name, message.author.name, message.author.id, message.content))
			f.write(s)

	@commands.command(hidden=True)
	@commands.guild_only()
	@checks.is_owner()
	async def removeallmsgs(self, ctx):
		async for log in ctx.message.channel.history():
			await log.delete()

	@commands.command()
	async def invite(self, ctx):
		try:
			await ctx.send("<https://discordapp.com/oauth2/authorize?&client_id=175432572271198208&scope=bot>")
		except:
			await ctx.message.author.send("https://discordapp.com/oauth2/authorize?&client_id=175432572271198208&scope=bot")

	@commands.command(aliases=['profilepic'])
	async def avatar(self, ctx):
		if len(ctx.message.mentions) > 0:
			await ctx.message.channel.send(ctx.message.mentions[0].avatar_url)
			return
		if len(ctx.message.content.split()) == 1:
				p = ctx.message.author.avatar_url
				await ctx.send(p)
		else:
			if discord.utils.find(lambda m: m.name.lower().startswith(ctx.message.content.split()[1].lower()), ctx.message.channel.guild.members) == None:
				await ctx.send('Person does not exist')
			else:
				p = discord.utils.find(lambda m: m.name.lower().startswith(ctx.message.content.split()[1].lower()), ctx.message.channel.guild.members).avatar_url
				await ctx.send(p)

	@commands.command()
	@commands.guild_only()
	async def info(self, ctx, *, member : discord.Member = None):
		if member is None:
			member = ctx.message.author
		dRol = ''
		dCol = -1
		dCol1 = member.roles[0]
		dJoin = member.joined_at
		for i in member.roles:
			dRol += i.name + '\n'
			if i.position > dCol:
				dCol1 = i
				dCol = i.position
		dCol2 = member.color
		dRol = dRol.strip('@everyone') #everyone has the @ everyone role by default so no need to show
		if dRol.startswith(', '):
			dRol = dRol[2:]
		p = member
		embed = discord.Embed()
		embed.color = dCol2.value
		if len(dRol.split()) == 0:
			dRol = 'None'
		embed.set_author(name=str(member), icon_url=str(member.avatar_url).replace("gif","png"))
		embed.add_field(name="Discord ID", value=p.id)
		embed.add_field(name="Roles", value=dRol)
		embed.add_field(name="Name Color", value=str(dCol2))
		embed.set_footer(text="Join Date", icon_url="https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png")
		embed.timestamp = dJoin

		await ctx.send(embed=embed)

	@commands.command(name='id')
	async def _id(self, ctx, *, member : discord.Member = None):
		if member is None:
			await ctx.send(ctx.message.author.id)
			return
		await ctx.send(member.id)

	@commands.command()
	async def emojibig(self, ctx, em : discord.Emoji = None):
		await ctx.send(em.url)

	@commands.command(name='stats')
	async def _stats(self,ctx):
		owner = self.bot.get_user(90886475373109248)
		embed = discord.Embed()
		embed.title = "Official BASEDBOT Discord guild"
		embed.url = "https://discord.gg/Gvt3Ks8"
		embed.set_author(name=str(owner), icon_url=str(owner.avatar_url).replace(".gif",".png"))

		s = str(len(self.bot.guilds))
		m = str(len(list(self.bot.get_all_members())))
		uniq = str(len(set(self.bot.get_all_members())))
		u = (datetime.now() - self.bot.uptime).total_seconds()
		min, sec = divmod(int(u), 60)
		h, min = divmod(min, 60)
		d, h = divmod(h, 24)
		t = "{} days\n{}:{}:{}".format(d,h,min,sec)

		embed.color = 13593328
		embed.add_field(name="guilds", value=s)
		embed.add_field(name="Members", value="{}\n{} unique".format(m,uniq))
		embed.add_field(name="Uptime", value=t)
		embed.set_footer(text='Made with discord.py', icon_url='http://i.imgur.com/5BFecvA.png')
		embed.timestamp = self.bot.uptime

		await ctx.send(embed=embed)
		
	@commands.command(enabled=False)
	@checks.in_dncd()
	async def raisehand(self, ctx):
		message = ctx.message
		mrole = discord.utils.get(message.guild.roles, name = 'Karaoke-Hand Raised')
		srole = discord.utils.get(message.guild.roles, name = 'Karaoke-Spotlight')
		rlist = []
		for i in message.author.roles:
			rlist.append(i.name)
		if 'Karaoke-Hand Raised' not in rlist:
			await message.author.add_roles(mrole)
			await ctx.send('You have raised your hand!')
			self.karaoke[0].append(message.author)
			if len(self.karaoke[0]) == 1:
				self.karaoke[1] = message.author
				await message.author.add_roles(srole)
		elif 'Karaoke-Hand Raised' in rlist:
			await message.author.remove_roles(mrole)
			await ctx.send('You have put down your hand!')
			try:
				self.karaoke[0].remove(message.author)
			except:
				pass
			try:
				await message.author.remove_roles(srole)
				if len(self.karaoke[0]) > 0:
					self.karaoke[1] = self.karaoke[0][0]
					await self.karaoke[1].add_roles(srole)
			except:
				pass
	@commands.command(enabled=False)
	@checks.in_dncd()
	async def klist(self, ctx):
		s = '```'
		for i in range(len(self.karaoke[0])):
			s += str(i+1) + '. ' + self.karaoke[0][i].name + '\n'
		s += '```'
		await ctx.send(s)

	@commands.command(enabled=False)
	@checks.in_dncd()
	@checks.dncd_mod()
	async def kskip(self, ctx):
		message = ctx.message
		mrole = discord.utils.get(message.guild.roles, name = 'Karaoke-Hand Raised')
		srole = discord.utils.get(message.guild.roles, name = 'Karaoke-Spotlight')
		await self.karaoke[0][0].remove_roles(mrole)
		await asyncio.sleep(1)
		await self.karaoke[0][0].remove_roles(srole)
		self.karaoke[0].pop(0)
		if len(self.karaoke[0]) > 0:
			self.karaoke[1] = self.karaoke[0][0]
			await self.karaoke[1].add_roles(srole)

	async def logmessage(self, message):
		await self.logM(message, message.channel.name)

	async def logM(self, message, cName):
		with io.open('C:/DISCORD BOT/message_logs/{}_Logs.txt'.format(cName),'a',encoding='utf-8') as f:
			logT = str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
			logM = ("{}({}) {}: {}\n".format(message.author.name, message.author.id, logT, message.content))
			f.write(logM)

	@commands.command(hidden=True)
	@checks.is_owner()
	async def debug(self, ctx, *, code : str):
		code = code.strip('` ')
		r = None
		env = {
			'bot': self.bot,
			'ctx': ctx,
			'message': ctx.message,
			'server': ctx.message.guild,
			'channel': ctx.message.channel,
			'author': ctx.message.author
		}
		env.update(globals())
		try:
			r = eval(code, env)
			if inspect.isawaitable(r):
				r = await r
		except Exception as e:
			await ctx.send("```py\n{}```".format(type(e).__name__ + ': ' + str(e)))
			return
		await ctx.send("```py\n{}```".format(r))

	@commands.command(aliases=['totalmeme','totalmember'], rest_is_raw=True)
	async def totalmem(self, ctx):
		await ctx.send("**Total Members:** {}".format(ctx.message.channel.guild.member_count))

	@commands.command()
	async def serverpic(self, ctx):
		embed = discord.Embed()
		embed.set_image(url=ctx.message.channel.guild.icon_url)
		await ctx.send(embed=embed)

	@commands.command(aliases=['channelid'])
	async def chid(self, ctx):
		await ctx.send(ctx.message.channel.id)

	@commands.command()
	async def serverid(self, ctx):
		await ctx.send(ctx.message.channel.guild.id)

	@commands.command(hidden=True)
	@checks.is_owner()
	async def msg(self, ctx, guild : int, * ,msg : str):
		await self.bot.get_guild(guild).get_channel(guild).send(msg)

	@commands.Cog.listener()
	async def on_message(self, message):
		if self.bot.user == message.author or message.channel.id == 168949939118800896 or message.author.id == 128044950024617984:
			return
		if isinstance(message.channel, discord.abc.PrivateChannel) == False:
			if message.channel.id in self.memeList:
				await self.memecheck(message)
		if isinstance(message.channel, discord.abc.PrivateChannel) == False and message.guild.id == 106293726271246336: #main server commands
			await self.logmessage(message)

	@commands.group()
	@checks.is_admin()
	async def welcome(self, ctx):
		if ctx.invoked_subcommand is None:
			await ctx.send("the `!welcome` command lets you customize/remove and relocate your welcome channel(only usable by admins)\n`!welcome off` < turns welcome message off\n`!welcome on` < turns on welcome channel and applies default settings, unless you had something previously saved\n`!welcome edit` < makes your custom welcome message, limit of 1.5k characters. type `!welcome edit` to see the format!\n`!welcome this` < allocates the welcome text to the text channel you invoked the command in\n`!welcome check` < shows your saved or default welcome message")

	@welcome.command(aliases=["off","disable"])
	async def W_off(self, ctx):
		sid = str(ctx.message.guild.id)
		if sid not in joins['disabled']:
			joins['disabled'].append(sid)
			with open('C:/DISCORD BOT/DiscordStuff/joins.json', 'w') as f:
				json.dump(joins, f, indent = 4)
			await ctx.send("Welcome message disabled")
		else:
			await ctx.send("Welcome message is already disabled")

	@welcome.command(aliases=["on","enable"])
	async def W_on(self, ctx):
		sid = str(ctx.message.guild.id)
		if sid in joins['disabled']:
			joins['disabled'].remove(sid)
			with open('C:/DISCORD BOT/DiscordStuff/joins.json', 'w') as f:
				json.dump(joins, f, indent = 4)
			await ctx.send("Welcome message enabled")
		else:
			await ctx.send("Welcome message is already enabled")

	@welcome.command(aliases=["this","here"])
	async def W_this(self, ctx):
		sid = str(ctx.message.guild.id)
		mid = str(ctx.message.channel.id)
		if joins.get(sid) is None:
			joins[sid] = {}
		if joins[sid].get("channel") == mid:
			await ctx.send("The welcome channel is already set to this channel.")
		else:
			joins[sid]["channel"] = mid
			with open('C:/DISCORD BOT/DiscordStuff/joins.json', 'w') as f:
				json.dump(joins, f, indent = 4)
			await ctx.send("Welcome message allocated to {}".format(ctx.message.channel.name))

	@welcome.command(aliases=["edit","modify","change"])
	async def W_edit(self, ctx, *, wm = None):
		sid = str(ctx.message.guild.id)
		if joins.get(sid) is None:
			joins[sid] = {}
		if wm == None:
			await ctx.send("You must give me input for the kind of welcome message you want.\n\nYou can have it include the person who joined's name with either `{name}` or `{mention}` and use `{server}` for the server name, or none.\n\nexample input if i joined a server named 'IMHUNGRY': `welcome new person named {name}, you have joined my great server named {server}!` would spit out \"welcome new person named BASEDBOT, you have joined my great server named IMHUNGRY!\"\n**Make sure to type the words encased in brackets in all lowercase**")
		elif len(wm) > 1500:
			await ctx.send("This message is greater than 1500 characters, make it smaller!")
		else:
			w = wm.replace("{name}", "{0.name}#{0.discriminator}").replace("{mention}", "{0.mention}").replace("{server}", "{0.guild.name}")
			joins[sid]["message"] = w
			with open('C:/DISCORD BOT/DiscordStuff/joins.json', 'w') as f:
				json.dump(joins, f, indent = 4)
			await ctx.send("Your welcome message ```\n{}```has been saved!".format(wm))

	@welcome.command(aliases=["show","check","message"])
	async def W_message(self, ctx):
		sid = str(ctx.message.guild.id)
		if joins.get(sid) is not None:
			if joins[sid].get("message") is not None:
				await ctx.send("Your saved message is ```\n{}```".format(joins[sid]['message']))
				return
		await ctx.send("Currently the default message is```\nWelcome {mention} to {server}!```")


	#LEAVE MESSAGES
	@commands.group()
	@checks.is_admin()
	async def leave(self, ctx):
		if ctx.invoked_subcommand is None:#default help message
			await ctx.send("the `!leave` command lets you customize/remove and relocate your leave channel(only usable by admins)\n`!leave off` < turns leave message off\n`!leave on` < turns on leave channel and applies default settings, unless you had something previously saved\n`!leave edit` < makes your custom leave message, limit of 1.5k characters. type `!leave edit` to see the format!\n`!leave this` < allocates the leave text to the text channel you invoked the command in\n`!leave check` < shows your saved or default leave message")

	@leave.command(aliases=["off","disable"])
	async def _off(self, ctx):
		sid = str(ctx.message.guild.id)
		if sid in leaves['enabled']:
			leaves['enabled'].remove(sid)
			with open('C:/DISCORD BOT/DiscordStuff/leaves.json', 'w') as f:
				json.dump(leaves, f, indent = 4)
			await ctx.send("leave message disabled")
		else:
			await ctx.send("leave message is already disabled")

	@leave.command(aliases=["on","enable"])
	async def _on(self, ctx):
		sid = str(ctx.message.guild.id)
		if sid not in leaves['enabled']:
			leaves['enabled'].append(sid)
			with open('C:/DISCORD BOT/DiscordStuff/leaves.json', 'w') as f:
				json.dump(leaves, f, indent = 4)
			await ctx.send("leave message enabled")
		else:
			await ctx.send("leave message is already enabled")

	@leave.command(aliases=["this","here"])
	async def _this(self, ctx):
		sid = str(ctx.message.guild.id)
		mid = ctx.message.channel.id
		if leaves.get(sid) is None:
			leaves[sid] = {}
		if leaves[sid].get("channel") == mid:
			await ctx.send("The leave channel is already set to this channel.")
		else:
			leaves[sid]["channel"] = mid
			with open('C:/DISCORD BOT/DiscordStuff/leaves.json', 'w') as f:
				json.dump(leaves, f, indent = 4)
			await ctx.send("leave message allocated to {}".format(ctx.message.channel.name))

	@leave.command(aliases=["edit","modify","change"])
	async def _edit(self, ctx, *, lm = None):
		sid = str(ctx.message.guild.id)
		if leaves.get(sid) is None:
			leaves[sid] = {}
		if lm == None:
			await ctx.send("You must give me input for the kind of leave message you want.\n\nYou can have it include the person who left's name with either `{name}` or `{mention}` and use `{server}` for the server name, or none.\n\nexample input if i left a server named 'IMHUNGRY': `bye bye new person named {name}, you have left my great server named {server}!` would spit out \"bye bye new person named BASEDBOT, you have left my great server named IMHUNGRY!\"\n**Make sure to type the words encased in brackets in all lowercase**")
		elif len(lm) > 1500:
			await ctx.send("This message is greater than 1500 characters, make it smaller!")
		else:
			l = lm.replace("{name}", "{0.name}#{0.discriminator}").replace("{mention}", "{0.mention}").replace("{server}", "{0.guild.name}")
			leaves[sid]["message"] = l
			with open('C:/DISCORD BOT/DiscordStuff/leaves.json', 'w') as f:
				json.dump(leaves, f, indent = 4)
			await ctx.send("Your leave message ```\n{}```has been saved!".format(lm))

	@leave.command(aliases=["show","message","check"])
	async def _message(self, ctx):
		sid = str(ctx.message.guild.id)
		if leaves.get(sid) is not None:
			if leaves[sid].get("message") is not None:
				await ctx.send("Your saved message is ```\n{}```".format(leaves[sid]['message']))
				return
		await ctx.send("Currently the default message is```\nGoodbye {name}!```")

	@commands.command()
	@checks.is_owner()
	async def testembeds(self, ctx):
		embed = discord.Embed()
		embed.color = 0xC3834C
		embed.title = "Welcome to the Dragon Nest Community Discord!"
		#embed.set_thumbnail(url="https://cdn.discordapp.com/icons/106293726271246336/060a9992637ea2724c166ef135fa6d83.jpg")
		embed.description = ("__**General Rules**__\n1. The Golden Rule applies: treat others as you would like to be treated.\n"
			"2. Please use primarily English in chat.\n"
			"3. Respect others. Deliberate provocation of others is not allowed. Friendly humor and \"ribbing\" are allowed, however both parties must be consenting and it should not be at someone else's expense.\n"
			"4. Try to keep discussions which have dedicated rooms in those rooms. Short quips in lounge are okay, but any involved conversation should be taken to that room. **If a moderator asks you to move to a room, move your conversation there.** Obscene material must be kept in designated channels. If you wish to not be able to access the 18 and above NSFW room, please let an Administrator or Moderator know.\n"
			"5. Controversial political, religious, etc discussions should go in a Discord server for that, not here.\n"
			"6. \"Doxing\" or revealing personal information of another user without their permission is a bannable offense.\n"
			"7. We have various \"bots\" in this Discord. Rules regarding bots are located below.\n"
			"8. Do not use proxies, duplicate accounts, or other methods to circumvent bans or timeouts.\n"
			"9. Do not impersonate another member without their explicit permission.\n"
			"10. No spamming. - Advertising your Discord channel without permission is also considered spamming\n"
			"11. No inappropriate or explicit avatars. Users may be asked to have their avatars changed or be removed from the server until compliance.\n\n"
			"Chronic abuse of the rules will result in a ban. The staff reserves the right to take any actions necessary to maintain the smooth operation of the Discord."
			)											
		embed.add_field(name="__Bot Rules__",value="1. Do not spam bot commands or intentionally cause spam using a bot.\n"
													"2. Please be tasteful about command use; occasional use of \"fun\" commands in <#106293726271246336> is fine, but beyond that please use the designated rooms.\n"
													"3. The owners/operators of the bots have full discretion on the use of their bots, including but not limited to: deciding what is considered abuse, allowing/denying users from using the bot, and what features are available.\n"
													"4. Bots must be authorized by the staff BEFORE joining. Unauthorized bots will be kicked and/or banned on sight."
													)
		embed.add_field(name="__Channel Specific Rules And Guidelines__",value="<#106301265817931776> - No gold or account buying/selling. We are not responsible for fraudulent transactions.")
		embed.add_field(name="__Opt in/out Channels__",value="Regarding #nsfw-18andabove please remember you can request to opt-out from seeing that channel if you frequent the Discord in less-than-desirable situations for porn\nIf you wish to discuss politics, contact a staff member to give you access to the #nsfw-political-discussion channel.")
		embed.add_field(name="__Links__",value="somestuff")
		await ctx.send(embed=embed)


class newmem(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def newmember(self, member):
		#if member.guild.id == 309953782920380416:
		#	mrole = discord.utils.get(member.guild.roles, name = "online")
		#	await member.add_roles(mrole)
		if str(member.guild.id) not in joins['disabled']:
			welcome_message = 'Welcome {0.mention} to {0.guild.name}!'
			welcome_channel = self.bot.get_channel(member.guild.id)
			if joins.get(str(member.guild.id)) is not None:
				welcome_channel = member.guild
				welcome_message = joins[str(member.guild.id)].get("message", welcome_message)
				welcome_channel = self.bot.get_channel(int(joins[str(member.guild.id)].get("channel", welcome_channel.id)))
			if welcome_message.count("{") == welcome_message.count("}") and welcome_message.count("{") != 0:
				welcome_message = welcome_message.format(member)
			try:
				await welcome_channel.send(welcome_message)
			except:
				pass
			t = datetime.now()
			if member.guild.id == 106293726271246336:
				with io.open('C:/DISCORD BOT/DiscordStuff/joinLog.txt','a',encoding='utf-8') as f:
					retS = "Name: {} ID: {} Time joined: {} EST\n".format(member.name, member.id, str(t))
					f.write(retS)

	@commands.Cog.listener()
	async def on_member_join(self, member):
		await self.newmember(member)


	async def removemember(self, member):
		if str(member.guild.id) in leaves['enabled']:
			leave_message = "Goodbye {0.name}#{0.discriminator}"
			leave_channel = self.bot.get_channel(member.guild.id)
			if leaves.get(str(member.guild.id)) is not None:
				leave_channel = member.guild
				leave_message = leaves[str(member.guild.id)].get("message", leave_message)
				leave_channel = leave_channel.get_channel(int(leaves[str(member.guild.id)].get("channel", leave_channel.id)))
			if leave_message.count("{") == leave_message.count("}") and leave_message.count("{") != 0:
				leave_message = leave_message.format(member)
			try:
				await leave_channel.send(leave_message)
			except:
				pass

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		await self.removemember(member)

def setup(bot):
	bot.add_cog(bbDiscord(bot))
	bot.add_cog(newmem(bot))