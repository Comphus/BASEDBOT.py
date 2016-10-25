import discord
import asyncio
import io
import time
import logging
from datetime import datetime, date, timedelta
logging.basicConfig()

sm = {'dncd':[False, 0]}
karaoke = [[], False]
dMods = []
with open('Mods.txt','r') as f:
	for i in f:
		dMods.append(str(i).replace('\n', ''))

class bbDiscord:

	
	def __init__(self, bot, message):
		self.bot = bot
		self.message = message

	async def slowmode(self):
		if self.message.author.id not in dMods:
			return
		if len(self.message.content.split()) == 2 and self.message.content.split()[1].isdigit() and 0 <= int(self.message.content.split()[1]) <= 30:
			sm['dncd'][1] = int(self.message.content.split()[1])
		try:				
			if type(3) == int(self.message.content.split()[1]): 
				if int(self.message.content.split()[1]) > 30:
					await self.bot.send_message(self.message.channel, "max limit is 30 seconds for slowmode")
					return
		except:
			pass
		if sm['dncd'][0]:
			await self.bot.send_message(self.message.channel, "slow mode is off!")
			sm['dncd'][0] = False
			for i in self.message.server.members:
				for j in i.roles:
					if 'slowmode' in j.name:
						await self.bot.remove_roles(i, discord.utils.find(lambda r: r.name == 'slowmode', self.message.channel.server.roles))
		else:
			if sm['dncd'][1] > 0:
				await self.bot.send_message(self.message.channel, "slow mode is on!")
			elif sm['dncd'][1] == 0:
				await self.bot.send_message(self.message.channel, "slow mode is on! Since no time interval was stated, the default of 15 seconds has been applied!")
				sm['dncd'][1] = 15
			sm['dncd'][0] = True

	async def startslowmode(self):
		if self.message.author.id in dMods:
			return
		await self.bot.add_roles(self.message.author, discord.utils.find(lambda r: r.name == 'slowmode', self.message.channel.server.roles))
		await asyncio.sleep(sm['dncd'][1])
		await self.bot.remove_roles(self.message.author, discord.utils.find(lambda r: r.name == 'slowmode', self.message.channel.server.roles))
		
	def slowM(self):
		return sm['dncd'][0]

	async def vanish(self):
		if (self.message.author.id in dMods or self.message.author.id in '105130465039548416' or self.message.author.server_permissions.administrator) == False:
			return
		if len(self.message.content.split()) != 3:
			await self.bot.send_message(self.message.channel, 'The format for !vanish is: "!vanish (@mention to person) (number of messages to delete)" and is only accessable to chatmods and above.')
			return
		cTime = datetime.now()
		logs = self.bot.logs_from(self.message.channel)
		counter = 0
		async for log in logs:
			if log.author.mention == self.message.mentions[0].mention:
				await self.bot.delete_message(log)
				counter += 1
			if counter == int(self.message.content.split()[2]):
				break
		with io.open('vanishlog.txt','a',encoding='utf-8') as f:
			s = ("{} {} Name: {} ID: {} What they wrote: {}\n".format(str(datetime.now().strftime("%m/%d/%Y %H:%M:%S")), self.message.server.name, self.message.author.name, self.message.author.id, self.message.content))
			f.write(s)
			
	async def removeallmsgs(self):
		logs =  self.bot.logs_from(self.message.channel)
		async for log in logs:
			await self.bot.delete_message(log)

	async def avatar(self):
		newR = self.message.content[8:]
		if len(self.message.mentions) > 0:
			await self.bot.send_message(self.message.channel, self.message.mentions[0].avatar_url)
			return
		if len(self.message.content.split()) == 1:
				p = self.message.author.avatar_url
				await self.bot.send_message(self.message.channel, p)
		else:
			if discord.utils.find(lambda m: m.name == newR, self.message.channel.server.members) == None:
				await self.bot.send_message(self.message.channel, 'Person does not exist')
			else:
				p = discord.utils.find(lambda m: m.name == newR, self.message.channel.server.members).avatar_url
				await self.bot.send_message(self.message.channel, p)

	async def info(self):
		dRol = ''
		dCol = -1
		p = discord.utils.find(lambda m: m.name == self.message.content[6:], self.message.channel.server.members)
		dCol1 = p.colour
		dJoin = p.joined_at
		for i in p.roles:
			dRol += i.name + ', '
			if i.position > dCol:
				dCol1 = i
				dCol = i.position
		dCol2 = str(dCol1.color)
		dRol = dRol[0:-2].replace('@everyone', '@-everyone')
		if dRol.startswith(', '):
			dRol = dRol[2:]
		await self.bot.send_message(self.message.channel, '```Name: {}\nID: {}\nDiscriminator: {}\nRoles: {}\nJoin Date: {}\nName Color: {}```'.format(p,p.id,p.discriminator,dRol,dJoin,str(dCol2)))


	async def myinfo(self):
		dRol = ''
		dCol = -1
		dCol1 = self.message.author.roles[0]
		dJoin = self.message.author.joined_at
		for i in self.message.author.roles:
			dRol += i.name + ', '
			if i.position > dCol:
				dCol1 = i
				dCol = i.position
		dCol2 = hex(dCol1.colour.value)
		dRol = dRol[0:-2].replace('@everyone', '@-everyone')
		if dRol.startswith(', '):
			dRol = dRol[2:]
		p = self.message.author
		await self.bot.send_message(self.message.channel, '```Name: {}\nID: {}\nDiscriminator: {}\nRoles: {}\nJoin Date: {}\nName Color: {}```'.format(p,p.id,p.discriminator,dRol,dJoin,str(dCol2)))

	async def dID(self):
		newR = self.message.content[4:]
		if len(self.message.content.split()) == 1:
			p = self.message.author.id
			await self.bot.send_message(self.message.channel, p)
		elif self.message.channel.is_private == False:
			if discord.utils.find(lambda m: m.name == newR, self.message.channel.server.members) == None:
				await self.bot.send_message(self.message.channel, 'Person does not exist, or you tried to mention them')
			else:
				p = discord.utils.find(lambda m: m.name == newR, self.message.channel.server.members).id
				await self.bot.send_message(self.message.channel, p)

	async def raisehand(self):
		mrole = discord.utils.get(self.message.server.roles, name = 'Karaoke-Hand Raised')
		srole = discord.utils.get(self.message.server.roles, name = 'Karaoke-Spotlight')
		rlist = []
		for i in self.message.author.roles:
			rlist.append(i.name)
		if 'Karaoke-Hand Raised' not in rlist:
			await self.bot.add_roles(self.message.author, mrole)
			await self.bot.send_message(self.message.channel, 'You have raised your hand!')
			karaoke[0].append(self.message.author)
			if len(karaoke[0]) == 1:
				karaoke[1] = self.message.author
				await self.bot.add_roles(self.message.author, srole)
		elif 'Karaoke-Hand Raised' in rlist:
			await self.bot.remove_roles(self.message.author, mrole)
			await self.bot.send_message(self.message.channel, 'You have put down your hand!')
			try:
				karaoke[0].remove(self.message.author)
			except:
				pass
			try:
				await self.bot.remove_roles(self.message.author, srole)
				if len(karaoke[0]) > 0:
					karaoke[1] = karaoke[0][0]
					await self.bot.add_roles(karaoke[1], srole)
			except:
				pass

	async def klist(self):
		s = '```'
		for i in range(len(karaoke[0])):
			s += str(i+1) + '. ' + karaoke[0][i].name + '\n'
		s += '```'
		await self.bot.send_message(self.message.channel, s)

	async def kskip(self):
		if self.message.author.id not in dMods:
			return
		mrole = discord.utils.get(self.message.server.roles, name = 'Karaoke-Hand Raised')
		srole = discord.utils.get(self.message.server.roles, name = 'Karaoke-Spotlight')
		await self.bot.remove_roles(karaoke[0][0], mrole)
		await asyncio.sleep(1)
		await self.bot.remove_roles(karaoke[0][0], srole)
		karaoke[0].pop(0)
		if len(karaoke[0]) > 0:
			karaoke[1] = karaoke[0][0]
			await self.bot.add_roles(karaoke[1], srole)

	async def logmessage(self):
		with io.open('chatLogs.txt','a',encoding='utf-8') as f:
			logT = str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
			logM = ("{}({}) {}: {}\n".format(self.message.author.name, self.message.author.id, logT, self.message.content))
			f.write(logM)

	async def debug(self):
		deb = self.message.content[7:]
		await self.bot.send_message(self.message.channel, str(eval(deb)))

class newmem():

	def __init__(self, bot, member):
		self.bot = bot
		self.member = member

	async def newmember(self):
		if self.member.server.id not in '82210263440306176 110373943822540800':
			try:
				if self.member.server.id not in '106293726271246336 148358898024316928':
					await client.send_message(self.member.server, 'Welcome {} to the server!'.format(self.member.mention))
			except:
				pass
			try:
				print(self.member)
			except:
				pass
			t = datetime.now()
			if str(self.member.server.id) == '106293726271246336':
				with io.open('joinLog.txt','a',encoding='utf-8') as f:
					retS = "Name: {} ID: {} Time joined: {} EST\n".format(self.member.name, self.member.id, str(t))
					f.write(retS)
