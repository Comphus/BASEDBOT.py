from discord.ext import commands
import discord
import asyncio
import io
import time
import logging
from datetime import datetime, date, timedelta
logging.basicConfig()

sm = {'dncd':[False, 0]}
karaoke = [[], False]
#upT = 0
dMods = []
with open('C:/DISCORD BOT/DiscordStuff/Mods.txt','r') as f:
	for i in f:
		dMods.append(str(i).replace('\n', ''))

def is_owner(ctx):
	return ctx.message.author.id == '90886475373109248'

class bbDiscord:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, hidden=True)
	async def slowmode(self, ctx):
		message = ctx.message
		if message.author.id not in dMods:
			return
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

	async def startslowmode(self, message):
		if message.author.id in dMods:
			return
		await self.bot.add_roles(message.author, discord.utils.find(lambda r: r.name == 'slowmode', message.channel.server.roles))
		await asyncio.sleep(sm['dncd'][1])
		await self.bot.remove_roles(message.author, discord.utils.find(lambda r: r.name == 'slowmode', message.channel.server.roles))
		
	def slowM(self):
		return sm['dncd'][0]

	async def on_message(self, message):
		if self.bot.user == message.author or message.channel.id == '168949939118800896' or message.author.id in '128044950024617984':
			return
		if message.channel.is_private == False and message.server.id == '106293726271246336': #main server commands
			await self.logmessage(message)
			if self.slowM():
				await self.startslowmode(message)

	@commands.command(pass_context=True, hidden=True)
	async def vanish(self, ctx):
		message = ctx.message
		if (message.author.id in dMods or message.author.id in '105130465039548416' or message.author.server_permissions.administrator) == False:
			return
		if len(message.content.split()) != 3:
			await self.bot.send_message(message.channel, 'The format for !vanish is: "!vanish (@mention to person) (number of messages to delete)" and is only accessable to chatmods and above.')
			return
		cTime = datetime.now()
		logs = self.bot.logs_from(message.channel)
		counter = 0
		async for log in logs:
			if log.author.mention == message.mentions[0].mention:
				await self.bot.delete_message(log)
				counter += 1
			if counter == int(message.content.split()[2]):
				break
		with io.open('C:/DISCORD BOT/DiscordStuff/vanishlog.txt','a',encoding='utf-8') as f:
			s = ("{} {} Name: {} ID: {} What they wrote: {}\n".format(str(datetime.now().strftime("%m/%d/%Y %H:%M:%S")), message.server.name, message.author.name, message.author.id, message.content))
			f.write(s)

	@commands.command(pass_context=True, hidden=True, no_pm=True)
	@commands.check(is_owner)
	async def removeallmsgs(self, ctx):
		logs =  self.bot.logs_from(ctx.message.channel)
		async for log in logs:
			await self.bot.delete_message(log)

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
			if discord.utils.find(lambda m: m.name == newR, message.channel.server.members) == None:
				await self.bot.say('Person does not exist')
			else:
				p = discord.utils.find(lambda m: m.name == newR, message.channel.server.members).avatar_url
				await self.bot.say(p)
	@commands.command(pass_context=True)
	async def myinfo(self, ctx):
		message = ctx.message
		dRol = ''
		dCol = -1
		dCol1 = message.author.roles[0]
		dJoin = message.author.joined_at
		for i in message.author.roles:
			dRol += i.name + '\n'
			if i.position > dCol:
				dCol1 = i
				dCol = i.position
		dCol2 = message.author.color
		dRol = dRol[0:-1].replace('@everyone', '')
		if dRol.startswith(', '):
			dRol = dRol[2:]
		p = message.author
		embed = discord.Embed()
		embed.color = dCol2.value
		embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
		embed.add_field(name="Discord ID", value=p.id)
		embed.add_field(name="Roles", value=dRol)
		embed.add_field(name="Name Color", value=str(dCol2))
		embed.set_footer(text="Join Date")
		embed.timestamp = dJoin

		await self.bot.say(embed=embed)
	@commands.command(name='id', pass_context=True)
	async def _id(self, ctx):
		newR = ctx.message.content[4:]
		if len(ctx.message.content.split()) == 1:
			p = ctx.message.author.id
			await self.bot.say(p)
		elif ctx.message.channel.is_private == False:
			if discord.utils.find(lambda m: m.name == newR, ctx.message.channel.server.members) == None:
				await self.bot.say('Person does not exist, or you tried to mention them')
			else:
				p = discord.utils.find(lambda m: m.name == newR, ctx.message.channel.server.members).id
				await self.bot.say(p)

	@commands.command(name='stats')
	async def _stats(self):
		owner = await self.bot.get_user_info('90886475373109248')
		embed = discord.Embed()
		embed.title = "Official BASEDBOT Discord Server"
		embed.url = "https://discord.gg/Gvt3Ks8"
		embed.set_author(name=str(owner), icon_url=owner.avatar_url)

		s = str(len(self.bot.servers))
		m = str(len(list(self.bot.get_all_members())))
		uniq = str(len(set(self.bot.get_all_members())))
		u = (datetime.now() - self.bot.uptime).total_seconds()
		t = str(time.strftime("%H:%M:%S", time.gmtime(u)))

		embed.color = 13593328
		embed.add_field(name="Servers", value=s)
		embed.add_field(name="Members", value="{}\n{} unique".format(m,uniq))
		embed.add_field(name="Uptime", value=t)
		embed.set_footer(text='Made with discord.py', icon_url='http://i.imgur.com/5BFecvA.png')
		embed.timestamp = self.bot.uptime

		await self.bot.say(embed=embed)
	@commands.command(pass_context=True, enabled=False)
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
	async def klist(self, ctx):
		s = '```'
		for i in range(len(karaoke[0])):
			s += str(i+1) + '. ' + karaoke[0][i].name + '\n'
		s += '```'
		await self.bot.say(s)

	@commands.command(pass_context=True, enabled=False)
	async def kskip(self, ctx):
		message = ctx.message
		if message.author.id not in dMods:
			return
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

	@commands.command(pass_context=True)
	async def debug(self, ctx):
		try:
			await self.bot.say(str(eval(ctx.message)))
		except Exception as e:
			await self.bot.say(e)

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

	@commands.command(pass_context=True)
	@commands.check(is_owner)
	async def msg(self, ctx):
		await self.bot.send_message(self.bot.get_server(ctx.message.content.split()[1]).default_channel, ctx.message.content.replace(ctx.message.content.split()[0], '').replace(ctx.message.content.split()[1], ''))



class newmem():
	def __init__(self, bot):
		self.bot = bot

	async def newmember(self, member):
		if member.server.id not in '82210263440306176 110373943822540800':
			try:
				if member.server.id not in '106293726271246336 148358898024316928':
					await self.bot.send_message(member.server, 'Welcome {} to the server!'.format(member.mention))
			except:
				pass
			try:
				print(member)
			except:
				pass
			t = datetime.now()
			if str(member.server.id) == '106293726271246336':
				with io.open('C:/DISCORD BOT/DiscordStuff/joinLog.txt','a',encoding='utf-8') as f:
					retS = "Name: {} ID: {} Time joined: {} EST\n".format(member.name, member.id, str(t))
					f.write(retS)

	async def on_member_join(self, member):
		await self.newmember(member)

def setup(bot):
	bot.add_cog(bbDiscord(bot))
	bot.add_cog(newmem(bot))
