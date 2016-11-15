import random
import requests
import json
import discord
import io
import asyncio
from datetime import datetime, date, timedelta
import time

with open("C:/DISCORD BOT/DiscordStuff/MainResponses.json") as j:
	MainResponses = json.load(j)

enhancing = {}
rtLimit = {}

class dragonnest:

	def __init__(self, bot, message):
		self.bot = bot
		self.message = message
		self.enhancefee = {
		0:[11, 3333, 3333, 100, 0],
		1:[28, 3333, 3333, 100, 1],
		2:[70, 3333, 3333, 100, 1],
		3:[140, 3333, 3333, 100, 1],
		4:[280, 3333, 3333, 100, 1],
		5:[560, 3333, 3333, 100, 1],
		6:[840, 3333, 3333, 100, 1],
		7:[1261, 3333, 3333, 100, 1],
		8:[1868, 3333, 3333, 100, 1],
		9:[2802, 3333, 3333, 100, 1],
		10:[3363, 2500, 3333, 3333, 1],
		11:[4340, 2000, 3333, 3333, 1],
		12:[4967, 1500, 3333, 3333, 2],
		13:[5716, 1000, 3333, 3333, 2],
		14:[6840, 500, 7999, 7999, 2]
		}
		self.ment = {
		'pug':['You have signed up for <#106300530548039680> mentions!','You have removed yourself from <#106300530548039680> mentions!','You can only mention the trade role in the <#106300530548039680> channel. This message will be deleted in 15 seconds'],
		'trade':['You have signed up for <#106301265817931776> mentions!', 'You have removed yourself from <#106301265817931776> mentions!', 'You can only mention the trade role in the <#106301265817931776> channel. This message will be deleted in 15 seconds'],
		'pvp':['You have signed up for <#106300621459628032> mentions!', 'You have removed yourself from <#106300621459628032> mentions!', 'You can only mention the pvp role in the <#106300621459628032> channel. This message will be deleted in 15 seconds'],
		'viewer':['You have signed up for Viewer mentions! Whenever a streamer goes online `BASEDBOT` will @ the role to notify you.','You have removed yourself from viewer mentions!','Only `BASEDBOT` can mention the Viewer role. This message will be deleted in 15 seconds']
		}

	def savednbuild(self):
		if self.message.content == ('!savednbuild') or self.message.content == ('!savednbuild '):
			return 'Your build must contain the format !savednbuild $(name of command) (tree build url)'
		elif (self.message.content.split()[-1].startswith('https://dnss.herokuapp.com') or self.message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') or self.message.content.split()[-1].startswith('https://dnmaze.com') or self.message.content.split()[-1].startswith('http://dnskillsim.herokuapp.com/') or self.message.content.split()[-1].startswith('https://dnskillsim.herokuapp.com/')) == False:
			return 'Your URL must be from dnskillsim.herokuapp.com,dnss.herokuapp.com, dnss-kr.herokuapp.com or https://dnmaze.com or is missing the https:// prefix'
		elif self.message.content.split()[1].startswith('$') == False:
			return 'Your command created command must have $ infront'
		elif len(str(self.message.content).split()) !=3:
			return 'Can only create a link with exactly 3 arguments'
		elif len(self.message.content.split()) == 3 and '$' in self.message.content.split()[1]: 
			with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','r+') as dnBuilds:
				for line in dnBuilds:
					if self.message.content.lower().split()[1] == line.lower().split()[1]:
						return 'A build with this name already exists!'
		dnBuildsSave = self.message.content.replace('!savednbuild ', '')
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','a') as bnsBuilds2:
			bnsBuilds2.write(str(self.message.author.id) + ' ' + dnBuildsSave + '\n')
			return 'build "'+self.message.content.split()[2]+'" saved! Use your command "'+self.message.content.split()[1]+'" to use it!'


	def editdnbuild(self):
		if self.message.content == ('!editdnbuild') or self.message.content == ('!editdnbuild '):
			return 'Your build must contain the format !editdnbuild $(name of command) (tree build url)'
		elif (self.message.content.split()[-1].startswith('https://dnss.herokuapp.com') or self.message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') or self.message.content.split()[-1].startswith('https://dnmaze.com') or self.message.content.split()[-1].startswith('http://dnskillsim.herokuapp.com/') or self.message.content.split()[-1].startswith('https://dnskillsim.herokuapp.com/')) == False:
			return 'Your URL must be from dnskillsim.herokuapp.com,dnss.herokuapp.com, dnss-kr.herokuapp.com or https://dnmaze.com or is missing the https:// prefix'
		elif len(self.message.content.split()) == 2 and self.message.content.split()[1].startswith('$'):
			return 'Your edited command must have $ infront'
		elif len(str(self.message.content).split()) !=3:
			return 'Can only edit a link with exactly 3 arguments'
		saveL = ''
		dnBuildsSave = self.message.content.replace('!editdnbuild ', '')
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','r') as bnsBuilds2:
			for line in bnsBuilds2:
				if self.message.content.split()[1] in line:
					if str(self.message.author.id) not in line:
						return 'This is not your build so you cannot edit it.'
					elif str(self.message.author.id) in line:
						saveL = line.rsplit(' ', 1)[0] + ' ' + self.message.content.split()[-1]
		saveL += '\n'
		newLines = []
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','r') as bnsBuilds2:
			for line in bnsBuilds2:
				if self.message.content.split()[1] not in line:
					newLines.append(line)
				else:
					newLines.append(saveL)
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','w') as bnsBuilds2:
			for line in newLines:
				bnsBuilds2.write(line)
		return 'build "'+self.message.content.split()[2]+'" has been edited! Use your command "'+self.message.content.split()[1]+'" to use it!'

	def deletednbuild(self):
		if self.message.content == ('!deletednbuild') or self.message.content == ('!deletednbuild '):
			return 'Your build must contain the format !deletednbuild $(name of command)'
		if len(self.message.content.split()) == 2 and self.message.content.split()[1].startswith('$') == False:
			return 'Your command created command must have $ infront'
		if len(str(self.message.content).split()) !=2:
			return 'Can only delete a link with exactly 2 arguments'
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','r') as bnsBuilds2:
			for line in bnsBuilds2:
				if self.message.content.split()[1] in line:
					if str(self.message.author.id) not in line:
						return 'This is not your build so you cannot delete it.'
		newLines = []
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','r') as bnsBuilds2:
			for line in bnsBuilds2:
				if self.message.content.split()[1] not in line:
					newLines.append(line)
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','w') as bnsBuilds2:
			for line in newLines:
				bnsBuilds2.write(line)
		return 'Your build ' + self.message.content.split()[-1] + ' has been deleted.'

	def prefixdncommands(self): #this is for the $ prefix
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt') as readBuilds:
			for line in readBuilds:
				if self.message.content.split()[0] == line.split()[-2]:
					return line.split()[-1]
	async def customdncommands(self):
		if self.prefixdncommands() == None:
			return
		else:
			await self.bot.send_message(self.message.channel, self.prefixdncommands())

	async def SA(self):
		await self.bot.send_message(self.message.channel, "https://docs.google.com/spreadsheets/d/1PMrzSRCuqBxOUsSpIUnh70-_uQRIkV3fZdOvaJ0rejc/edit#gid=29")

	async def enhancement(self):
		if 'stop' in self.message.content.lower():
			await self.bot.send_message(self.message.channel, "I have reset your enhancing progress")
			enhancing[self.message.author.id] = [0, 0, 0]
			return
		if self.message.author.id not in enhancing:
			enhancing[self.message.author.id] = [0, 0, 0]
		if self.message.author.id in enhancing:
			if enhancing[self.message.author.id][0] == 15:
				await self.bot.send_message(self.message.channel, "Your weapon is a +15, you won the game. Resetting progress!")
				enhancing[self.message.author.id] = [0, 0, 0]
				return
			dotdot = [". .",". . ."]
			m = await self.bot.send_message(self.message.channel, "Enhancing your LV80 L-Grade weapon **.**")
			await asyncio.sleep(.7)
			for i in range(2):
				await self.bot.edit_message(m, "Enhancing your LV80 L-Grade weapon **{}**".format(dotdot[i]))
				await asyncio.sleep(.7)
			tryagain = True
			while tryagain:
				a = random.randint(1, 10000)
				b = random.randint(1, 10000)
				c = random.randint(1, 10000)
				d = random.randint(1, 10000)
				if a <= self.enhancefee[enhancing[self.message.author.id][0]][1] and b <= self.enhancefee[enhancing[self.message.author.id][0]][2]:
					continue
				if b <= self.enhancefee[enhancing[self.message.author.id][0]][2] and c <= self.enhancefee[enhancing[self.message.author.id][0]][3]:
					if enhancing[self.message.author.id][0] < 13:
						degrade = 0
						if enhancing[self.message.author.id][0] > 0:
							degrade = random.randint(1, self.enhancefee[enhancing[self.message.author.id][0]][4])
						enhancing[self.message.author.id][1] += self.enhancefee[enhancing[self.message.author.id][0]][0]
						enhancing[self.message.author.id][0] -= degrade
						enhancing[self.message.author.id][2] += 1
						await self.bot.edit_message(m, "Enhancement __**Failed AND Decreased!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} gold** with __{}__ attempts.".format(enhancing[self.message.author.id][0], enhancing[self.message.author.id][1], enhancing[self.message.author.id][2]))
						tryagain = False
						return
					elif enhancing[self.message.author.id][0] >= 13:
						if d <= self.enhancefee[enhancing[self.message.author.id][0]][2]:
							enhancing[self.message.author.id][1] += self.enhancefee[enhancing[self.message.author.id][0]][0]
							enhancing[self.message.author.id][0] = 0
							enhancing[self.message.author.id][2] += 1
							await self.bot.edit_message(m, "__**WEAPON BROKE!**__ Enhancement level is now 0, but gold and attempts will remain! Your L-Grade is now **+{}**\nYou have spent a total of **{} gold** with __{}__ attempts.".format(enhancing[self.message.author.id][0], enhancing[self.message.author.id][1], enhancing[self.message.author.id][2]))
							tryagain = False
							return
						elif d > self.enhancefee[enhancing[self.message.author.id][0]][2]:
							degrade = random.randint(0, self.enhancefee[enhancing[self.message.author.id][0]][4])
							enhancing[self.message.author.id][1] += self.enhancefee[enhancing[self.message.author.id][0]][0]
							enhancing[self.message.author.id][0] -= degrade
							enhancing[self.message.author.id][2] += 1
							await self.bot.edit_message(m, "Enhancement __**Failed AND Decreased!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} gold** with __{}__ attempts.".format(enhancing[self.message.author.id][0], enhancing[self.message.author.id][1], enhancing[self.message.author.id][2]))
							tryagain = False
							return
				if b <= self.enhancefee[enhancing[self.message.author.id][0]][2]:
					if enhancing[self.message.author.id][0] < 13:
						enhancing[self.message.author.id][1] += self.enhancefee[enhancing[self.message.author.id][0]][0]
						enhancing[self.message.author.id][2] += 1
						await self.bot.edit_message(m, "Enhancement __**Failed!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} gold** with __{}__ attempts.".format(enhancing[self.message.author.id][0], enhancing[self.message.author.id][1], enhancing[self.message.author.id][2]))
						tryagain = False
						return
					elif enhancing[self.message.author.id][0] >= 13:
						if d <= self.enhancefee[enhancing[self.message.author.id][0]][2]:
							enhancing[self.message.author.id][1] += self.enhancefee[enhancing[self.message.author.id][0]][0]
							enhancing[self.message.author.id][0] = 0
							enhancing[self.message.author.id][2] += 1
							await self.bot.edit_message(m, "__**WEAPON BROKE!**__ Enhancement level is now 0, but gold and attempts will remain! Your L-Grade is now **+{}**\nYou have spent a total of **{} gold** with __{}__ attempts.".format(enhancing[self.message.author.id][0], enhancing[self.message.author.id][1], enhancing[self.message.author.id][2]))
							tryagain = False
							return
						elif d > self.enhancefee[enhancing[self.message.author.id][0]][2]:
							enhancing[self.message.author.id][1] += self.enhancefee[enhancing[self.message.author.id][0]][0]
							enhancing[self.message.author.id][2] += 1
							await self.bot.edit_message(m, "Enhancement __**Failed!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} gold** with __{}__ attempts.".format(enhancing[self.message.author.id][0], enhancing[self.message.author.id][1], enhancing[self.message.author.id][2]))
							tryagain = False
							return
				if a <= self.enhancefee[enhancing[self.message.author.id][0]][1]:
					enhancing[self.message.author.id][1] += self.enhancefee[enhancing[self.message.author.id][0]][0]
					enhancing[self.message.author.id][0] += 1
					enhancing[self.message.author.id][2] += 1
					await self.bot.edit_message(m, "Enhancement __**Successful!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} gold** with __{}__ attempts.".format(enhancing[self.message.author.id][0], enhancing[self.message.author.id][1], enhancing[self.message.author.id][2]))
					tryagain = False
					return

	def mdb(self):
		numbercount = 1
		returnbox = []
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt') as readBuilds:
			for line in readBuilds:
				if str(self.message.author.id) in line or str(self.message.author) in line:
					returnbox.append(str(numbercount)+': '+line.replace(str(self.message.author.id)+ ' ', ''))
					numbercount += 1
		if len(returnbox) == 0:
			return ['You have no saved builds!']
		else:
			return returnbox
	async def mydnbuilds(self):
		for line in self.mdb():
			await self.bot.send_message(self.message.channel, line)

	def skillbuilds(self):
		if self.message.content.lower().startswith('!skillbuilds'):
			dnClass = self.message.content.lower().replace('!skillbuilds ', '')
		elif self.message.content.lower().startswith('!krskillbuilds'):
			dnClass = self.message.content.lower().replace('!krskillbuilds ', '')
		if '!skillbuilds' == self.message.content.lower().split()[0] and len(self.message.content.split()) == 1:
			return 'https://dnskillsim.herokuapp.com/na'
		elif '!krskillbuilds' == self.message.content.lower().split()[0] and len(self.message.content.split()) == 1:
			return 'https://dnskillsim.herokuapp.com/kdn'
		else:
			try:
				if self.message.content.lower().startswith('!skillbuilds'):
					return 'http://dnskillsim.herokuapp.com/na/{}'.format(MainResponses["dnskillbuilds"][dnClass])
				elif self.message.content.lower().startswith('!krskillbuilds'):
					return 'http://dnskillsim.herokuapp.com/kdn/{}'.format(MainResponses["t5dnskillbuilds"][dnClass])
			except:	
				return '2nd argument not recognised'

	async def autobuilds(self):
		requestedBuild = []
		requestedBuilds = []
		m = self.message.content.lower()
		if 'build' in m and '?' in m and len(m.split()) > 1:
			m = m.replace('build', ' ')
			for i in MainResponses["t5dnskillbuilds"].values():
				if i in m:
					requestedBuild.append(i)
					m = m.replace(i, '')
			for i in MainResponses["t5dnskillbuilds"]:
				if i in m:
					requestedBuild.append(MainResponses["t5dnskillbuilds"][i])
					m = m.replace(MainResponses["t5dnskillbuilds"][i], '')
		if len(requestedBuild) == 0:
			return
		else:
			for i in requestedBuild:
				if i not in requestedBuilds:
					requestedBuilds.append(i)
			pmlist = []
			missingb = []
			noB = False
			with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','r') as b:
				readB = b.readlines()
				for i in requestedBuilds:
					checksB = 0
					for line in readB:
						if i in line.split()[-1]:
							try:
								pmlist.append(line.replace(line.split()[0], discord.utils.get(self.message.server.members, id = line.split()[0]).name))
								checksB += 1
							except:
								pmlist.append(line.replace(line.split()[0], 'Unknown User'))
								checksB += 1
					if checksB == 0:
						missingb.append(i)
						noB = True
					checksB = 0
			if len(pmlist) == 0:
				await self.bot.send_message(self.message.channel, 'There appears to be no build for the class(es) requested :(')
			else:
				await self.bot.send_message(self.message.channel, 'I have PMed you a list of community saved build(s) for {}'.format(requestedBuilds))
				if noB == True:
					await self.bot.send_message(self.message.channel, 'However, there appears to be no build(s) made for {} :('.format(missingb))
				for i in pmlist:
					await self.bot.send_message(self.message.author, i)

	async def onoffrole(self, mess):
		mrole = discord.utils.get(self.message.server.roles, name = mess)
		rlist = []
		for i in self.message.author.roles:
			rlist.append(i.name)
		if mess not in rlist:
			await self.bot.add_roles(self.message.author, mrole)
			await self.bot.send_message(self.message.channel, '{}'.format(self.ment[mess][0]))
		elif mess in rlist:
			await self.bot.remove_roles(self.message.author, mrole)
			await self.bot.send_message(self.message.channel, '{}'.format(self.ment[mess][1]))
	
	async def roleMention(self, mess):
		m = await self.bot.send_message(self.message.channel, "{} {}".format(self.message.author.mention, self.ment[mess][2]))
		with io.open('C:/DISCORD BOT/DiscordStuff/attempts.txt','a',encoding='utf-8') as attempts:
			attempts.write('{}({}) attempted to mention {} on {}UTC outside of the {} channel. They said: {}\n'.format(self.message.author.id, self.message.author.name, ('@'+mess), str(self.message.timestamp), mess, self.message.content))
		await self.bot.delete_message(self.message)
		await asyncio.sleep(15)
		await self.bot.delete_message(m)

class streamer:

	def __init__(self, bot, member):
		self.bot = bot
		self.member = member

	async def DNstream(self):
		if self.member.id not in list(rtLimit.keys()):
			rtLimit[self.member.id] = None
		if rtLimit[self.member.id] == None or (datetime.now() - rtLimit[self.member.id]).total_seconds() // 3600 >= 2:
			rtLimit[self.member.id] = datetime.now()
			r = requests.get('https://api.twitch.tv/kraken/streams/{}/?&client_id=4asyzu8i1l7ea1f61aebw3mgbuv04y2'.format(self.member.game.url.replace('https://www.twitch.tv/', '')))
			tData = r.json()
			await self.bot.send_message(self.bot.get_channel('106293726271246336'), "<@&246470826675666944> **{}#{}** has started streaming **{}**!\nThey're playing **{}**, Come watch them at <{}>".format(self.member.name, self.member.discriminator, self.member.game.name,tData['stream']['game'], self.member.game.url))
			print('something happened with {} for stream'.format(self.member.id))
