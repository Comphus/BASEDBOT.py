from discord.ext import commands
import discord
from .utils import checks
import asyncio
import inspect
import io
import time
import logging
import codecs
import json
from datetime import datetime, date, timedelta
logging.basicConfig()

dMods = []
with open('C:/DISCORD BOT/DiscordStuff/Mods.txt','r') as f:
	for i in f:
		dMods.append(i.strip('\n'))
with open('C:/DISCORD BOT/DiscordStuff/joins.json') as f:
	joins = json.load(f)
with open('C:/DISCORD BOT/DiscordStuff/leaves.json') as f:
	leaves = json.load(f)
sm = {'dncd':[False, 0]}
karaoke = [[], False]
memeList = {}
class bbDiscord:
	"""
	discord functions for BASEDBOT
	"""
	def __init__(self, bot):
		self.bot = bot

	async def startslowmode(self, message):
		if message.author.id in dMods:
			return
		await self.bot.add_roles(message.author, discord.utils.find(lambda r: r.name == 'slowmode', message.channel.server.roles))
		await asyncio.sleep(sm['dncd'][1])
		await self.bot.remove_roles(message.author, discord.utils.find(lambda r: r.name == 'slowmode', message.channel.server.roles))
		
	def slowM(self):
		return sm['dncd'][0]

	@commands.command(pass_context=True, hidden=True)
	@checks.dncd_mod()
	async def slowmode(self, ctx):
		message = ctx.message
		if len(message.content.split()) == 2 and message.content.split()[1].isdigit() and 0 <= int(message.content.split()[1]) <= 30:
			sm['dncd'][1] = int(message.content.split()[1])
		try:				
			if type(3) == int(message.content.split()[1]): 
				if int(message.content.split()[1]) > 30:
					await self.bot.send_message(message.channel, "max limit is 30 seconds for slowmode")
					return
		except:
			pass
		if 'off' in message.content.lower():
			await self.bot.send_message(message.channel, "slow mode is off!")
			sm['dncd'][0] = False
			for i in message.server.members:
				for j in i.roles:
					if 'slowmode' in j.name:
						await self.bot.remove_roles(i, discord.utils.find(lambda r: r.name == 'slowmode', message.channel.server.roles))
		else:
			if sm['dncd'][1] > 0:
				await self.bot.say("slow mode is on!")
			elif sm['dncd'][1] == 0:
				await self.bot.say("slow mode is on! Since no time interval was stated, the default of 15 seconds has been applied!")
				sm['dncd'][1] = 15
			sm['dncd'][0] = True

	@commands.command(pass_context=True)
	@checks.dncd_mod_or_admin()
	async def meme(self, ctx):
		message = ctx.message
		if message.channel.id not in memeList:
			memeList[message.channel.id] = True
			await self.bot.say("meme mode is on!")
			return
		if memeList[message.channel.id] == True:
			memeList[message.channel.id] = False
			await self.bot.say("meme mode is off!")
		else:
			memeList[message.channel.id] = True
			await self.bot.say("meme mode is on!")

	async def memecheck(self, message):
		if memeList[message.channel.id] == True:
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
				await self.bot.delete_message(message)

	@commands.command(pass_context=True, hidden=True, no_pm=True)
	@checks.dncd_mod_or_admin()
	async def purge(self, ctx, num : int = 50):
		await self.bot.purge_from(ctx.message.channel, limit=num)


	@commands.command(pass_context=True, hidden=True, no_pm=True)
	@checks.dncd_mod_or_admin()
	async def vanish(self, ctx):
		message = ctx.message
		van = 0
		if len(message.content.split()) not in (3,2):
			await self.bot.send_message(message.channel, 'The format for !vanish is: "!vanish (@mention to person(nothing if yourself)) (number of messages to delete)" and is only accessable to chatmods and above.')
			return
		if message.content.split()[-1].isdigit():
			van = int(message.content.split()[-1])
		elif message.content.split()[1].isdigit():
			van = int(message.content.split()[1])
		else:
			await self.bot.send_message(message.channel, 'The format for !vanish is: "!vanish (@mention to person(nothing if yourself)) (number of messages to delete)" and is only accessable to chatmods and above.')
			return
		mem = None
		if len(message.content.split()) == 2:
			mem = message.author
		else:
			try:
				mem = message.mentions[0]
			except:
				await self.bot.send_message(message.channel, 'The format for !vanish is: "!vanish (@mention to person(nothing if yourself)) (number of messages to delete)" and is only accessable to chatmods and above.')
				return
		cTime = datetime.now()
		logs = self.bot.logs_from(message.channel)
		counter = 0
		async for log in logs:
			if log.author == mem:
				await self.bot.delete_message(log)
				counter += 1
			if counter == van:
				break
		with io.open('C:/DISCORD BOT/DiscordStuff/vanishlog.txt','a',encoding='utf-8') as f:
			s = ("{} {} Name: {} ID: {} What they wrote: {}\n".format(str(datetime.now().strftime("%m/%d/%Y %H:%M:%S")), message.server.name, message.author.name, message.author.id, message.content))
			f.write(s)

	@commands.command(pass_context=True, hidden=True, no_pm=True)
	@checks.is_owner()
	async def removeallmsgs(self, ctx):
		logs = self.bot.logs_from(ctx.message.channel)
		async for log in logs:
			await self.bot.delete_message(log)

	@commands.command()
	async def invite(self):
		try:
			await self.bot.say("https://discordapp.com/oauth2/authorize?&client_id=175432572271198208&scope=bot")
		except:
			await self.bot.whisper("https://discordapp.com/oauth2/authorize?&client_id=175432572271198208&scope=bot")

	@commands.command(pass_context=True)
	async def avatar(self, ctx):
		message = ctx.message
		newR = message.content[8:]
		if len(message.mentions) > 0:
			await self.bot.send_message(message.channel, message.mentions[0].avatar_url)
			return
		if len(message.content.split()) == 1:
				p = message.author.avatar_url
				await self.bot.say(p)
		else:
			if discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members) == None:
				await self.bot.say('Person does not exist')
			else:
				p = discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).avatar_url
				await self.bot.say(p)
	@commands.command(pass_context=True, no_pm=True)
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
		if member.avatar_url != '':
			embed.set_author(name=str(member), icon_url=member.avatar_url)
		else:
			embed.set_author(name=str(member), icon_url=member.default_avatar_url)
		embed.add_field(name="Discord ID", value=p.id)
		embed.add_field(name="Roles", value=dRol)
		embed.add_field(name="Name Color", value=str(dCol2))
		embed.set_footer(text="Join Date", icon_url="https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png")
		embed.timestamp = dJoin

		await self.bot.say(embed=embed)
	@commands.command(name='id', pass_context=True)
	async def _id(self, ctx, *, member : discord.Member = None):
		if member is None:
			await self.bot.say(ctx.message.author.id)
			return
		await self.bot.say(member.id)

	@commands.command()
	async def emojibig(self, em : discord.Emoji = None):
		await self.bot.say(em.url)
	@commands.command(name='stats')
	async def _stats(self):
		owner = await self.bot.get_user_info('90886475373109248')
		embed = discord.Embed()
		embed.title = "Official BASEDBOT Discord Server"
		embed.url = "https://discord.gg/Gvt3Ks8"
		embed.set_author(name=str(owner), icon_url=owner.avatar_url.replace(".gif",".png"))

		s = str(len(self.bot.servers))
		m = str(len(list(self.bot.get_all_members())))
		uniq = str(len(set(self.bot.get_all_members())))
		u = (datetime.now() - self.bot.uptime).total_seconds()
		t = str(time.strftime("%d days\n%H:%M:%S", time.gmtime(u)))

		embed.color = 13593328
		embed.add_field(name="Servers", value=s)
		embed.add_field(name="Members", value="{}\n{} unique".format(m,uniq))
		embed.add_field(name="Uptime", value=t)
		embed.set_footer(text='Made with discord.py', icon_url='http://i.imgur.com/5BFecvA.png')
		embed.timestamp = self.bot.uptime

		await self.bot.say(embed=embed)
	@commands.command(pass_context=True, enabled=False)
	@checks.in_dncd()
	async def raisehand(self, ctx):
		message = ctx.message
		mrole = discord.utils.get(message.server.roles, name = 'Karaoke-Hand Raised')
		srole = discord.utils.get(message.server.roles, name = 'Karaoke-Spotlight')
		rlist = []
		for i in message.author.roles:
			rlist.append(i.name)
		if 'Karaoke-Hand Raised' not in rlist:
			await self.bot.add_roles(message.author, mrole)
			await self.bot.say('You have raised your hand!')
			karaoke[0].append(message.author)
			if len(karaoke[0]) == 1:
				karaoke[1] = message.author
				await self.bot.add_roles(message.author, srole)
		elif 'Karaoke-Hand Raised' in rlist:
			await self.bot.remove_roles(message.author, mrole)
			await self.bot.say('You have put down your hand!')
			try:
				karaoke[0].remove(message.author)
			except:
				pass
			try:
				await self.bot.remove_roles(message.author, srole)
				if len(karaoke[0]) > 0:
					karaoke[1] = karaoke[0][0]
					await self.bot.add_roles(karaoke[1], srole)
			except:
				pass
	@commands.command(pass_context=True, enabled=False)
	@checks.in_dncd()
	async def klist(self, ctx):
		s = '```'
		for i in range(len(karaoke[0])):
			s += str(i+1) + '. ' + karaoke[0][i].name + '\n'
		s += '```'
		await self.bot.say(s)

	@commands.command(pass_context=True, enabled=False)
	@checks.in_dncd()
	@checks.dncd_mod()
	async def kskip(self, ctx):
		message = ctx.message
		mrole = discord.utils.get(message.server.roles, name = 'Karaoke-Hand Raised')
		srole = discord.utils.get(message.server.roles, name = 'Karaoke-Spotlight')
		await self.bot.remove_roles(karaoke[0][0], mrole)
		await asyncio.sleep(1)
		await self.bot.remove_roles(karaoke[0][0], srole)
		karaoke[0].pop(0)
		if len(karaoke[0]) > 0:
			karaoke[1] = karaoke[0][0]
			await self.bot.add_roles(karaoke[1], srole)

	async def logmessage(self, message):
		await self.logM(message, message.channel.name)

	async def logM(self, message, cName):
		with io.open('C:/DISCORD BOT/message_logs/{}_Logs.txt'.format(cName),'a',encoding='utf-8') as f:
			logT = str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
			logM = ("{}({}) {}: {}\n".format(message.author.name, message.author.id, logT, message.content))
			f.write(logM)

	@commands.command(pass_context=True, hidden=True)
	@checks.is_owner()
	async def debug(self, ctx, *, code : str):
		code = code.strip('` ')
		r = None
		env = {
			'bot': self.bot,
			'ctx': ctx,
			'message': ctx.message,
			'server': ctx.message.server,
			'channel': ctx.message.channel,
			'author': ctx.message.author
		}
		env.update(globals())
		try:
			r = eval(code, env)
			if inspect.isawaitable(r):
				r = await r
		except Exception as e:
			await self.bot.say("```py\n{}```".format(type(e).__name__ + ': ' + str(e)))
			return
		await self.bot.say("```py\n{}```".format(r))

	@commands.command(pass_context = True, aliases=['totalmeme','totalmember'], rest_is_raw=True)
	async def totalmem(self, ctx):
		await self.bot.say("**Total Members:** {}".format(ctx.message.channel.server.member_count))

	@commands.command(pass_context=True)
	async def serverpic(self, ctx):
		embed = discord.Embed()
		embed.set_image(url=ctx.message.channel.server.icon_url)
		await self.bot.say(embed=embed)

	@commands.command(pass_context=True, aliases=['channelid'])
	async def chid(self, ctx):
		await self.bot.say(ctx.message.channel.id)

	@commands.command(pass_context=True)
	async def serverid(self, ctx):
		await self.bot.say(ctx.message.channel.server.id)

	@commands.command(pass_context=True, hidden=True)
	@checks.is_owner()
	async def msg(self, ctx):
		await self.bot.send_message(self.bot.get_server(ctx.message.content.split()[1]).default_channel, ctx.message.content.replace(ctx.message.content.split()[0], '').replace(ctx.message.content.split()[1], ''))

	async def on_message(self, message):
		if self.bot.user == message.author or message.channel.id == '168949939118800896' or message.author.id in '128044950024617984':
			return
		if message.channel.is_private == False and message.server.id == '106293726271246336': #main server commands
			await self.logmessage(message)
			if self.slowM():
				await self.startslowmode(message)
			if message.channel.id in memeList:
				await self.memecheck(message)

	@commands.group(pass_context=True)
	@checks.is_admin()
	async def welcome(self, ctx):
		print("check")
		if ctx.invoked_subcommand is None:
			await self.bot.say("the `!welcome` command lets you customize/remove and relocate your welcome channel(only usable by admins)\n`!welcome off` < turns welcome message off\n`!welcome on` < turns on welcome channel and applies default settings, unless you had something previously saved\n`!welcome edit` < makes your custom welcome message, limit of 1.5k characters. type `!welcome edit` to see the format!\n`!welcome this` < allocates the welcome text to the text channel you invoked the command in\n`!welcome check` < shows your saved or default welcome message")

	@welcome.command(pass_context=True, aliases=["off","disable"])
	async def W_off(self, ctx):
		sid = ctx.message.server.id
		print("hello")
		if sid not in joins['disabled']:
			joins['disabled'].append(sid)
			with open('C:/DISCORD BOT/DiscordStuff/joins.json', 'w') as f:
				json.dump(joins, f, indent = 4)
			await self.bot.say("Welcome message disabled")
		else:
			await self.bot.say("Welcome message is already disabled")

	@welcome.command(pass_context=True, aliases=["on","enable"])
	async def W_on(self, ctx):
		sid = ctx.message.server.id
		if sid in joins['disabled']:
			joins['disabled'].remove(sid)
			with open('C:/DISCORD BOT/DiscordStuff/joins.json', 'w') as f:
				json.dump(joins, f, indent = 4)
			await self.bot.say("Welcome message enabled")
		else:
			await self.bot.say("Welcome message is already enabled")

	@welcome.command(pass_context=True, aliases=["this","here"])
	async def W_this(self, ctx):
		sid = ctx.message.server.id
		mid = ctx.message.channel.id
		if joins.get(sid) is None:
			joins[sid] = {}
		if joins[sid].get("channel") == mid:
			await self.bot.say("The welcome channel is already set to this channel.")
		else:
			joins[sid]["channel"] = mid
			with open('C:/DISCORD BOT/DiscordStuff/joins.json', 'w') as f:
				json.dump(joins, f, indent = 4)
			await self.bot.say("Welcome message allocated to {}".format(ctx.message.channel.name))

	@welcome.command(pass_context=True, aliases=["edit","modify","change"])
	async def W_edit(self, ctx, *, wm = None):
		sid = ctx.message.server.id
		if joins.get(sid) is None:
			joins[sid] = {}
		if wm == None:
			await self.bot.say("You must give me input for the kind of welcome message you want.\n\nYou can have it include the person who joined's name with either `{name}` or `{mention}` and use `{server}` for the server name, or none.\n\nexample input if i joined a server named 'IMHUNGRY': `welcome new person named {name}, you have joined my great server named {server}!` would spit out \"welcome new person named BASEDBOT, you have joined my great server named IMHUNGRY!\"\n**Make sure to type the words encased in brackets in all lowercase**")
		elif len(wm) > 1500:
			await self.bot.say("This message is greater than 1500 characters, make it smaller!")
		else:
			w = wm.replace("{name}", "{0.name}#{0.discriminator}").replace("{mention}", "{0.mention}").replace("{server}", "{0.server.name}")
			joins[sid]["message"] = w
			with open('C:/DISCORD BOT/DiscordStuff/joins.json', 'w') as f:
				json.dump(joins, f, indent = 4)
			await self.bot.say("Your welcome message ```\n{}```has been saved!".format(wm))

	@welcome.command(pass_context=True, aliases=["show","check","message"])
	async def W_message(self, ctx):
		sid = ctx.message.server.id
		if joins.get(sid) is not None:
			if joins[sid].get("message") is not None:
				await self.bot.say("Your saved message is ```\n{}```".format(joins[sid]['message']))
				return
		await self.bot.say("Currently the default message is```\nWelcome {mention} to {server}!```")


	#LEAVE MESSAGES
	@commands.group(pass_context=True)
	@checks.is_admin()
	async def leave(self, ctx):
		if ctx.invoked_subcommand is None:#default help message
			await self.bot.say("the `!leave` command lets you customize/remove and relocate your leave channel(only usable by admins)\n`!leave off` < turns leave message off\n`!leave on` < turns on leave channel and applies default settings, unless you had something previously saved\n`!leave edit` < makes your custom leave message, limit of 1.5k characters. type `!leave edit` to see the format!\n`!leave this` < allocates the leave text to the text channel you invoked the command in\n`!leave check` < shows your saved or default leave message")

	@leave.command(pass_context=True, aliases=["off","disable"])
	async def _off(self, ctx):
		sid = ctx.message.server.id
		if sid in leaves['enabled']:
			leaves['enabled'].append(sid)
			with open('C:/DISCORD BOT/DiscordStuff/leaves.json', 'w') as f:
				json.dump(leaves, f, indent = 4)
			await self.bot.say("leave message disabled")
		else:
			await self.bot.say("leave message is already disabled")

	@leave.command(pass_context=True, aliases=["on","enable"])
	async def _on(self, ctx):
		sid = ctx.message.server.id
		if sid not in leaves['enabled']:
			leaves['enabled'].append(sid)
			with open('C:/DISCORD BOT/DiscordStuff/leaves.json', 'w') as f:
				json.dump(leaves, f, indent = 4)
			await self.bot.say("leave message enabled")
		else:
			await self.bot.say("leave message is already enabled")

	@leave.command(pass_context=True, aliases=["this","here"])
	async def _this(self, ctx):
		sid = ctx.message.server.id
		mid = ctx.message.channel.id
		if leaves.get(sid) is None:
			leaves[sid] = {}
		if leaves[sid].get("channel") == mid:
			await self.bot.say("The leave channel is already set to this channel.")
		else:
			leaves[sid]["channel"] = mid
			with open('C:/DISCORD BOT/DiscordStuff/leaves.json', 'w') as f:
				json.dump(leaves, f, indent = 4)
			await self.bot.say("leave message allocated to {}".format(ctx.message.channel.name))

	@leave.command(pass_context=True, aliases=["edit","modify","change"])
	async def _edit(self, ctx, *, lm = None):
		sid = ctx.message.server.id
		if leaves.get(sid) is None:
			leaves[sid] = {}
		if lm == None:
			await self.bot.say("You must give me input for the kind of leave message you want.\n\nYou can have it include the person who left's name with either `{name}` or `{mention}` and use `{server}` for the server name, or none.\n\nexample input if i left a server named 'IMHUNGRY': `bye bye new person named {name}, you have left my great server named {server}!` would spit out \"bye bye new person named BASEDBOT, you have left my great server named IMHUNGRY!\"\n**Make sure to type the words encased in brackets in all lowercase**")
		elif len(lm) > 1500:
			await self.bot.say("This message is greater than 1500 characters, make it smaller!")
		else:
			l = lm.replace("{name}", "{0.name}#{0.discriminator}").replace("{mention}", "{0.mention}").replace("{server}", "{0.server.name}")
			leaves[sid]["message"] = l
			with open('C:/DISCORD BOT/DiscordStuff/leaves.json', 'w') as f:
				json.dump(leaves, f, indent = 4)
			await self.bot.say("Your leave message ```\n{}```has been saved!".format(lm))

	@leave.command(pass_context=True, aliases=["show","message","check"])
	async def _message(self, ctx):
		sid = ctx.message.server.id
		if leaves.get(sid) is not None:
			if leaves[sid].get("message") is not None:
				await self.bot.say("Your saved message is ```\n{}```".format(leaves[sid]['message']))
				return
		await self.bot.say("Currently the default message is```\nGoodbye {name}!```")


class newmem():
	def __init__(self, bot):
		self.bot = bot

	async def newmember(self, member):
		if member.server.id not in joins['disabled']:
			welcome_message = 'Welcome {0.mention} to {0.server.name}!'
			welcome_channel = member.server
			if joins.get(member.server.id) is not None:
				welcome_message = joins[member.server.id].get("message", welcome_message)
				welcome_channel = self.bot.get_channel(joins[member.server.id].get("channel", welcome_channel.id))
			if welcome_message.count("{") == welcome_message.count("}") and welcome_message.count("{") != 0:
				welcome_message = welcome_message.format(member)
			try:
				await self.bot.send_message(welcome_channel, welcome_message)
			except:
				pass
			t = datetime.now()
			if member.server.id == '106293726271246336':
				with io.open('C:/DISCORD BOT/DiscordStuff/joinLog.txt','a',encoding='utf-8') as f:
					retS = "Name: {} ID: {} Time joined: {} EST\n".format(member.name, member.id, str(t))
					f.write(retS)

	async def on_member_join(self, member):
		await self.newmember(member)


	async def removemember(self, member):
		if member.server.id in leaves['enabled']:
			leave_message = "Goodbye {0.name}#{0.discriminator}"
			leave_channel = member.server
			if leaves.get(member.server.id) is not None:
				leave_message = leaves[member.server.id].get("message", leave_message)
				leave_channel = self.bot.get_channel(leaves[member.server.id].get("channel", leave_channel.id))
			if leave_message.count("{") == leave_message.count("}") and leave_message.count("{") != 0:
				leave_message = leave_message.format(member)
			try:
				await self.bot.send_message(leave_channel, leave_message)
			except:
				pass

	async def on_member_remove(self, member):
		await self.removemember(member)

def setup(bot):
	bot.add_cog(bbDiscord(bot))
	bot.add_cog(newmem(bot))
