import random
import aiohttp
import json
import discord
from discord.ext import commands
from .utils import checks
from bs4 import BeautifulSoup
import io
import asyncio
from datetime import datetime, date, timedelta
import time
import re

with open("C:/DISCORD BOT/DiscordStuff/MainResponses.json") as j:
	MainResponses = json.load(j)
with open('C:/DISCORD BOT/DragonNest/DNbuilds.json') as f:
	dnBuilds = json.load(f)

enhancing = {}
rtLimit = {}

class dragonnest(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.enhancefee = {#put this and ment in MainResponses
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
		'viewer':['You have signed up for Viewer mentions! Whenever a streamer goes online `BASEDBOT` will @ the role to notify you.','You have removed yourself from viewer mentions!','Only `BASEDBOT` can mention the Viewer role. This message will be deleted in 15 seconds'],
		'showdown':['You have signed up for Showdown mentions!', 'You have removed yourself from Showdown mentions!'],
		'dnfeed':['You have subscribed to `DNFeed` notifications!','You have unsubscribed from `DNFeed` notifications!','Only `BASEDBOT` can mention the `DNFeed` role. This message will be deleted in 15 seconds']
		}
		self.colors ={
		"update":0x40AA01,
		"maint.":0xda99d9,
		"event":0xffb816,
		"notice":0x12A1F3
		}
		self.theTask = None
		self.buildURLs = [
			"https://dnskillsim.herokuapp.com/",
			"http://dnskillsim.herokuapp.com/"
		]#there used to be multiple skill build sites, but it looks like everyone just uses 1 now



	def sdb(self, ctx, cmd, url, desc):
		if None in (cmd,url) or not cmd.startswith("$"):
			return 'Your build must contain the format `!savednbuild $(name_of_command) (tree_build_url) (optional_description)`'
		elif not any(i in url for i in self.buildURLs):
			return 'Your URL must be from `https://dnskillsim.herokuapp.com/` or is missing the https:// prefix'
		missingClass = 1
		for i in MainResponses["t5dnskillbuilds"].values(): #i = classes
			if i in url:
				missingClass = 0
				if "build_names" not in dnBuilds:
					dnBuilds["build_names"] = {}
				if cmd not in dnBuilds["build_names"]:
					dnBuilds["build_names"][cmd] = {"cls":i,"id":ctx.message.author.id}
				else:
					return 'A build with this name already exists!'

				if i not in dnBuilds:
					dnBuilds[i] = {}
				dnBuilds[i][cmd] = {
						"id":ctx.message.author.id,
						"url":url,
						"desc":desc
					}
				break
			if missingClass:
				return 'Could not find that class, tell Comphus to update list.'
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.json','w') as f:
			json.dump(dnBuilds, f, indent = 4)
			return "Build `{}` successfully saved".format(cmd)

		"""
		dnBuildsSave = message.content.replace('!savednbuild ', '').replace('!savebuild ', '')
		with open('C:/DISCORD BOT/DragonNest/DNbuilds.txt','a') as bnsBuilds2:
			bnsBuilds2.write(str(message.author.id) + ' ' + dnBuildsSave + '\n')
			return 'build "'+message.content.split()[-1]+'" saved! Use your command "'+message.content.split()[1]+'" to use it!'
		"""

	@commands.command(aliases=['savebuild'])
	async def savednbuild(self, ctx, command_name = None, url = None, *, desc = ""):
		await ctx.send(self.sdb(ctx, command_name, url, desc))


	def edb(self, ctx, cmd, url, desc):
		if None in (cmd,url) or not cmd.startswith("$"):
			return 'Your build must contain the format `!editdnbuild $(name_of_command) (tree_build_url) (optional_description)`'
		elif not any(i in url for i in self.buildURLs):
			return 'Your URL must be from `https://dnskillsim.herokuapp.com/` or is missing the https:// prefix'

		if cmd not in dnBuilds["build_names"]:
			return "cannot find the command `{}`, use `!savednbuild` to save a build".format(cmd)
		if ctx.message.author.id != dnBuilds["build_names"][cmd]["id"]:
			return 'This is not your build so you cannot edit it.'

		missingClass = 1
		for i in MainResponses["t5dnskillbuilds"].values(): #i = classes
			if i in url:
				missingClass = 0
				if i != dnBuilds["build_names"][cmd]["cls"]:
					dnBuilds[dnBuilds["build_names"][cmd]["cls"]].pop(cmd, None)
				dnBuilds["build_names"][cmd]["cls"] = i
				if i not in dnBuilds:
					dnBuilds[i] = {}
				dnBuilds[i][cmd] = {
						"id":ctx.message.author.id,
						"url":url,
						"desc":desc
					}
				break
		if missingClass:
			return 'Could not find that class, tell Comphus to update list.'

		with open('C:/DISCORD BOT/DragonNest/DNbuilds.json','w') as f:
			json.dump(dnBuilds, f, indent = 4)
			return "Build `{}` successfully edited".format(cmd)


	@commands.command(aliases=['editbuild'])
	async def editdnbuild(self, ctx, command_name = None, url = None, *, desc = ""):
		await ctx.send(self.edb(ctx, command_name, url, desc))

	def ddb(self, ctx, cmd):#can use jsons with this, make it so its in a json, everyone can have whatever name they want, but if they have clashing build names then it chooses the one of whoever casted it
		if not cmd or not cmd.startswith("$"):
			return 'Your build must contain the format `!deletednbuild $(name_of_command)`'

		if cmd not in dnBuilds["build_names"]:
			return "cannot find the command `{}`".format(cmd)
		if ctx.message.author.id != dnBuilds["build_names"][cmd]["id"]:
			return 'This is not your build so you cannot delete it.'

		dnBuilds[dnBuilds["build_names"][cmd]["cls"]].pop(cmd, None)
		dnBuilds["build_names"].pop(cmd, None)


		with open('C:/DISCORD BOT/DragonNest/DNbuilds.json','w') as f:
			json.dump(dnBuilds, f, indent = 4)
			return "Build `{}` successfully deleted".format(cmd)

	@commands.command(aliases=['deletebuild'])
	async def deletednbuild(self, ctx, command_name = None):
		await ctx.send(self.ddb(ctx, command_name))

	async def prefixdncommands(self, message): #this is for the $ prefix, also, cache this
		try:
			if message.content.split()[0] in dnBuilds["build_names"]:
				cmd = message.content.split()[0]
				build = dnBuilds[dnBuilds["build_names"][cmd]['cls']][cmd]
				p = self.bot.get_user(build["id"])
				embed = discord.Embed()
				if build['desc']:
					embed.description=build['desc']
				embed.title = cmd
				embed.url = build['url']
				embed.color = p.color.value
				embed.set_author(name=str(p), icon_url=str(p.avatar_url))
				embed.set_footer(text='Dragon Nest', icon_url='http://i.imgur.com/0zURV1B.png')
				return embed
		except:
			pass

	#@commands.command(command_prefix='$)
	async def customdncommands(self, message):
		s = await self.prefixdncommands(message)
		if not s:
			return
		await message.channel.send(embed=s)

	@commands.command(aliases=['spring'])
	async def springs(self,ctx):
		await ctx.send("http://i.imgur.com/BAAv8F7.png")

	@commands.command()
	async def reita(self, ctx):
		await ctx.send(file=discord.File("C:/DISCORD BOT/DragonNest/reita.png", "reita.png"))

	@commands.command()
	async def sa(self, ctx, *,skill : str = None):
		if skill is None:
			await ctx.send("https://docs.google.com/spreadsheets/d/1PMrzSRCuqBxOUsSpIUnh70-_uQRIkV3fZdOvaJ0rejc/edit#gid=29")
		else:
			ac = ['lv','normal','special','alternate','level','left click','part']
			cl = ['warrior','archer','sorceress','cleric','academic','kali','assassin','lancer','machina']
			s = skill.lower()
			colms = [0,7,8]
			with open("C:/DISCORD BOT/DragonNest/SA.json") as j:
				a = json.load(j)
			saName = []
			saVal = []
			saBreak = []
			for name in cl:
				for i in range(len(a[name])):
					if i == 0 or i == 1:
						continue
					try:
						for z in colms:
							if not not a[name][i][z] and s in str(a[name][i][z]).lower():
								saName.append(a[name][i][z])
								saVal.append(a[name][i][z+1])
								saBreak.append(a[name][i][z+2])
								c = 1
								while True:
									d = 0
									for k in ac:
										if k in a[name][i+c][z].lower():
											saName.append(a[name][i+c][z])
											saVal.append(a[name][i+c][z+1])
											saBreak.append(a[name][i+c][z+2])
											c += 1
										else:
											d += 1
									if d == len(ac):
										break
					except:
						pass
			if len(saName) == 0:
				await ctx.send("I couldnt find that skill")
				return
			embed = discord.Embed()
			embed.title = saName[0]
			embed.url = 'https://docs.google.com/spreadsheets/d/1PMrzSRCuqBxOUsSpIUnh70-_uQRIkV3fZdOvaJ0rejc/edit#gid=29'
			embed.color = 16718105
			saN = ''
			saV = ''
			saB = ''
			for i in range(len(saName)):
				if not saName[i]:
					saN += "None\n"
				else:
					saN += str(saName[i]) + '\n'
				if i not in saVal or not saVal[i]:
					saV += "None\n"
				else:
					saV += str(saVal[i]) + '\n'
				if i not in saBreak or not saBreak[i]:
					saB += "None\n"
				else:
					saB += str(saBreak[i]) + '\n'
			embed.add_field(name="Skill", value=saN)
			embed.add_field(name="SA Break", value=saV)
			embed.add_field(name="SA", value=saB)
			embed.set_footer(text='Dragon Nest Super Armor', icon_url='http://i.imgur.com/0zURV1B.png')
			await ctx.send(embed=embed)

	
	async def emojihance(self, message, m):
		await m.remove_reaction("🔨", message.author)
		dotdot = [".",". .",". . ."]
		for i in range(3):
			await m.edit(content="Enhancing your LV80 L-Grade weapon **{}**".format(dotdot[i]))
			await asyncio.sleep(.7)
		await self.enhanceweapon(message, m)
		def pred(r, m):
			return m == message.author and r.emoji == "🔨"
		try:
			user, rec = await self.bot.wait_for('reaction_add', check=pred, timeout=60)
		except asyncio.TimeoutError:
			await ctx.send("reaction timed out!")
			await m.remove_reaction("🔨", self.bot.user)
			return
		else:
			await self.emojihance(message, m)


	#@commands.command(aliases=["!pvp","!PVP"])
	#async def help_pvp(self):
			
	@commands.command()
	#@checks.not_lounge()
	async def enhance(self, ctx):
		message = ctx.message
		if 'stop' in message.content.lower():
			await ctx.send("I have reset your enhancing progress")
			enhancing[message.author.id] = [0, 0, 0, message]
			return
		if message.author.id not in enhancing:
			enhancing[message.author.id] = [0, 0, 0, message]
		if message.author.id in enhancing:
			if enhancing[message.author.id][0] == 15:
				await ctx.send("Your weapon is a +15, you won the game. Resetting progress!")
				enhancing[message.author.id] = [0, 0, 0, message]
				return
			dotdot = [". .",". . ."]
			m = await ctx.send("Enhancing your LV80 L-Grade weapon **.**")
			await asyncio.sleep(.7)
			for i in range(2):
				await m.edit(content="Enhancing your LV80 L-Grade weapon **{}**".format(dotdot[i]))
				await asyncio.sleep(.7)
			await self.enhanceweapon(message, m)
			await m.add_reaction("🔨")
			def pred(r, m):
				return m == message.author and r.emoji == "🔨"
			try:
				user, rec = await self.bot.wait_for('reaction_add', check=pred, timeout=60)
			except asyncio.TimeoutError:
				await ctx.send("reaction timed out!")
				await m.remove_reaction("🔨", self.bot.user)
				return
			else:
				await self.emojihance(message, m)

	async def enhanceweapon(self, message, m):
		tryagain = True
		while tryagain:#just a var to name what the enhance thingy does, can just write True
			a = random.randint(1, 10000) #the succ
			b = random.randint(1, 10000) #fail rate rate
			c = random.randint(1, 10000) #degrade rate
			d = random.randint(1, 10000)
			if a <= self.enhancefee[enhancing[message.author.id][0]][1] and b <= self.enhancefee[enhancing[message.author.id][0]][2]:
				continue
			if b <= self.enhancefee[enhancing[message.author.id][0]][2] and c <= self.enhancefee[enhancing[message.author.id][0]][3]:
				if enhancing[message.author.id][0] < 13:
					degrade = 0
					if enhancing[message.author.id][0] > 0:
						degrade = random.randint(1, self.enhancefee[enhancing[message.author.id][0]][4])
					enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]
					enhancing[message.author.id][0] -= degrade
					enhancing[message.author.id][2] += 1
					await m.edit(content="Enhancement __**Failed AND Decreased!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} {}** with __{}__ attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], '<:VipGold:248714191517646848>', enhancing[message.author.id][2]))
					tryagain = False
					return
				elif enhancing[message.author.id][0] >= 13:
					if d <= self.enhancefee[enhancing[message.author.id][0]][2]:
						enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]
						enhancing[message.author.id][0] = 0
						enhancing[message.author.id][2] += 1
						await m.edit(content="__**WEAPON BROKE!**__ Enhancement level is now 0, but gold and attempts will remain! Your L-Grade is now **+{}**\nYou have spent a total of **{} {}** with __{}__ attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], '<:VipGold:248714191517646848>', enhancing[message.author.id][2]))
						tryagain = False
						return
					elif d > self.enhancefee[enhancing[message.author.id][0]][2]:
						degrade = random.randint(0, self.enhancefee[enhancing[message.author.id][0]][4])
						enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]
						enhancing[message.author.id][0] -= degrade
						enhancing[message.author.id][2] += 1
						await m.edit(content="Enhancement __**Failed AND Decreased!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} {}** with __{}__ attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], '<:VipGold:248714191517646848>', enhancing[message.author.id][2]))
						tryagain = False
						return
			if b <= self.enhancefee[enhancing[message.author.id][0]][2]:
				if enhancing[message.author.id][0] < 13:
					enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]
					enhancing[message.author.id][2] += 1
					await m.edit(content="Enhancement __**Failed!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} {}** with __{}__ attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], '<:VipGold:248714191517646848>', enhancing[message.author.id][2]))
					tryagain = False
					return
				elif enhancing[message.author.id][0] >= 13:
					if d <= self.enhancefee[enhancing[message.author.id][0]][2]:
						enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]
						enhancing[message.author.id][0] = 0
						enhancing[message.author.id][2] += 1
						await m.edit(content="__**WEAPON BROKE!**__ Enhancement level is now 0, but gold and attempts will remain! Your L-Grade is now **+{}**\nYou have spent a total of **{} {}** with __{}__ attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], '<:VipGold:248714191517646848>', enhancing[message.author.id][2]))
						tryagain = False
						return
					elif d > self.enhancefee[enhancing[message.author.id][0]][2]:
						enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]
						enhancing[message.author.id][2] += 1
						await m.edit(content="Enhancement __**Failed!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} {}** with __{}__ attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], '<:VipGold:248714191517646848>', enhancing[message.author.id][2]))
						tryagain = False
						return
			if a <= self.enhancefee[enhancing[message.author.id][0]][1]:
				enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]
				enhancing[message.author.id][0] += 1
				enhancing[message.author.id][2] += 1
				await m.edit(content="Enhancement __**Successful!**__ Your L-Grade is now **+{}**\nYou have spent a total of **{} {}** with __{}__ attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], '<:VipGold:248714191517646848>', enhancing[message.author.id][2]))
				tryagain = False
				return


	@commands.command(aliases=['dragonegg'])
	@checks.not_lounge()
	async def egg(self, ctx):
		r = random.randint(0,len(MainResponses['egg'])-1)
		embed = discord.Embed()
		embed.set_author(name='​', icon_url=MainResponses['egg'][r][0])
		embed.set_footer(text='Dragon Egg Simulator', icon_url='http://i.imgur.com/jw1voOg.png')
		m = await ctx.send(embed=embed)
		for i in range(3):
			await asyncio.sleep(0.3)
			r = random.randint(0,len(MainResponses['egg'])-1)
			embed = discord.Embed()
			embed.set_author(name='​',icon_url=MainResponses['egg'][r][0])
			embed.set_footer(text='Dragon Egg Simulator', icon_url='http://i.imgur.com/jw1voOg.png')
			await m.edit(embed=embed)
		await asyncio.sleep(2)
		r = random.randint(0,9998)
		if r <= 6812:#these ifs are cases to see how rare of an item they get, following the KR %s
			while True:
				r = random.randint(0,len(MainResponses['egg'])-1)
				if MainResponses['egg'][r][2] == 0 or MainResponses['egg'][r][2] == 4871440:
					await self.eggres(m,r)
					break
		elif r <= 8862:
			while True:
				r = random.randint(0,len(MainResponses['egg'])-1)
				if MainResponses['egg'][r][2] == 5804481:
					await self.eggres(m,r)
					break
		elif r <= 9566:
			while True:
				r = random.randint(0,len(MainResponses['egg'])-1)
				if MainResponses['egg'][r][2] == 13400111:
					await self.eggres(m,r)
					break
		else:
			while True:
				r = random.randint(0,len(MainResponses['egg'])-1)
				if MainResponses['egg'][r][2] == 6363561:
					await self.eggres(m,r)
					break

	async def eggres(self, m, r):
		embed = discord.Embed()
		embed.set_author(name=MainResponses['egg'][r][1],icon_url=MainResponses['egg'][r][0])
		embed.color = MainResponses['egg'][r][2]
		embed.set_footer(text='Dragon Egg Simulator', icon_url='http://i.imgur.com/jw1voOg.png')
		await m.edit(embed=embed)

	@commands.command(aliases=['mybuilds'])
	async def mydnbuilds(self, ctx):
		message = ctx.message
		numbercount = 1
		returnbox = ''
		for cmd in dnBuilds["build_names"]:
			if message.author.id == dnBuilds["build_names"][cmd]["id"]:
				returnbox +='{}. [{}]({})\n'.format(numbercount,cmd,dnBuilds[dnBuilds["build_names"][cmd]["cls"]][cmd]["url"])
				numbercount += 1
		if returnbox == '':
			await ctx.send('You have no saved builds!')
		else:
			embed = discord.Embed(description=returnbox)
			embed.color = message.author.color.value
			embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
			embed.set_footer(text='Dragon Nest', icon_url='http://i.imgur.com/0zURV1B.png')
			await ctx.send(embed=embed)

	@commands.command(aliases = ['krskillbuilds'])
	async def skillbuilds(self, ctx, *, build : str = None):
		message = ctx.message
		if build is None:
			if '!skillbuilds' == message.content.lower().split()[0]:
				await ctx.send('https://spacem.github.io/dnskillsim/build-search/?region=na&jobId=64%3F')
			else:
				await ctx.send('https://spacem.github.io/dnskillsim/build-search/?region=kdn&jobId=64%3F')
			return
		if message.content.lower().startswith('!skillbuilds'):
			try:
				await ctx.send('http://dnskillsim.herokuapp.com/na/{}'.format(MainResponses["dnskillbuilds"][build.lower()]))
				return
			except:
				pass
		else:
			try:
				await ctx.send('http://dnskillsim.herokuapp.com/kdn/{}'.format(MainResponses["t5dnskillbuilds"][build.lower()]))
				return
			except:
				pass
		await ctx.send('2nd argument not recognised')

	async def autobuilds(self, message):
		requestedBuild = []
		requestedBuilds = []
		m = message.content.lower()
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
			for i in requestedBuilds:
				checksB = 0
				try:
					for entry in dnBuilds[i]:
						ent = dnBuilds[i][entry]
						pmlist.append({"name":entry,"url":ent["url"],"desc":ent["desc"],"user":self.bot.get_user(ent["id"])})
						checksB += 1
				except:
					pass
				if checksB == 0:
					missingb.append(i)
					noB = True
				checksB = 0
			if len(pmlist) == 0:
				await message.add_reaction("❌")
				#await message.channel.send('There appears to be no build for the class(es) requested :(')
			else:
				await message.add_reaction("✅")
				#await message.channel.send('I have PMed you a list of community saved build(s) for {}'.format(requestedBuilds))
				if noB == True:
					await message.add_reaction("⚠")
					await message.author.send("No builds were found for the following class(es): {}".format(missingb))
					#await message.channel.send('However, there appears to be no build(s) made for {} :('.format(missingb))
				for i in pmlist:
					embed = discord.Embed()
					if not i["desc"]:
						desc = "No Description."
					else:
						desc = i["desc"]
					embed.description = desc
					embed.title = i["name"]
					embed.url = i["url"]
					embed.color = 13593328
					try:
						embed.set_author(name=str(i["user"]), icon_url=str(i["user"].avatar_url))
					except:
						pass
					embed.set_footer(text='Dragon Nest', icon_url='http://i.imgur.com/0zURV1B.png')
					await message.author.send(embed = embed)

	async def onoffrole(self, mess, message):
		mrole = discord.utils.get(message.guild.roles, name = mess)
		rlist = []
		for i in message.author.roles:
			rlist.append(i.name)
		if mess not in rlist:
			await message.author.add_roles(mrole)
			await message.channel.send('{}'.format(self.ment[mess][0]))
		elif mess in rlist:
			await message.author.remove_roles(mrole)
			await message.channel.send('{}'.format(self.ment[mess][1]))
	
	async def roleMention(self, mess, message):
		m = await message.channel.send("{} {}".format(message.author.mention, self.ment[mess][2]))
		with io.open('C:/DISCORD BOT/DiscordStuff/attempts.txt','a',encoding='utf-8') as attempts:
			attempts.write('{}({}) attempted to mention {} on {}UTC outside of the {} channel. They said: {}\n'.format(message.author.id, message.author.name, ('@'+mess), str(datetime.now()), mess, message.content))
		await message.delete()
		await asyncio.sleep(15)
		await m.delete()

	@commands.command()
	async def pug(self, ctx):
		if ctx.message.channel.id != 106293726271246336 and ctx.message.channel.guild.id == 106293726271246336:
			await self.onoffrole('pug', ctx.message)
	@commands.command()
	async def showdown(self, ctx):
		if ctx.message.channel.id != 106293726271246336 and ctx.message.channel.guild.id == 106293726271246336:
			await self.onoffrole('showdown', ctx.message)
	@commands.command()
	async def trade(self, ctx):
		if ctx.message.channel.id != 106293726271246336:
			await self.onoffrole('trade', ctx.message)
	@commands.command()
	async def pvp(self, ctx):
		if ctx.message.channel.id != 106293726271246336:
			await self.onoffrole('pvp', ctx.message)
	@commands.command()
	async def viewer(self, ctx):
		if ctx.message.guild.id == 106293726271246336:
			await self.onoffrole('viewer', ctx.message)
	@commands.command()
	async def dnfeed(self, ctx):
		if ctx.message.guild.id == 106293726271246336:
			await self.onoffrole('dnfeed', ctx.message)
			
	@commands.Cog.listener()
	async def on_message(self, message):
		if self.bot.user == message.author or message.channel.id == 168949939118800896 or message.author.id == 128044950024617984:
			return
		if '@pug' in message.clean_content and message.channel.id != 106300530548039680 and message.channel.guild.id == 106293726271246336:
			await self.roleMention('pug', message)
		if '@trade' in message.clean_content and message.channel.id != 106301265817931776 and message.channel.guild.id == 106293726271246336:
			await self.roleMention('trade', message)
		if '@pvp' in message.clean_content and message.channel.id != 106300621459628032 and message.channel.guild.id == 106293726271246336:
			await self.roleMention('pvp', message)
		if '@viewer' in message.clean_content and message.channel.guild.id == 106293726271246336:
			await self.roleMention('viewer', message)
		if '@dnfeed' in message.clean_content and message.channel.guild.id == 106293726271246336 and message.author.id != 90886475373109248:
			await self.roleMention('dnfeed', message)
		if message.channel.id == 107718615452618752:
			await self.autobuilds(message)
		elif message.content.startswith('$') and len(message.content.split()) == 1:
			await self.customdncommands(message)	

class streamer(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def DNstream(self, before, after):#redo this with the commands ext now that commands ext docs exist
		if len(before.roles) == len(after.roles):
			for i in after.roles:
				if i.name.lower() == 'streamer':
					if after.activity is not None and after.activity.type == 1:
						if after.guild.id not in rtLimit:
							rtLimit[after.guild.id] = {}
						if after.id not in list(rtLimit[after.guild.id].keys()):
							rtLimit[after.guild.id][after.id] = None
						if rtLimit[after.guild.id][after.id] == None or (datetime.now() - rtLimit[after.guild.id][after.id]).total_seconds() // 3600 >= 2:
							rtLimit[after.guild.id][after.id] = datetime.now()
							try:
								async with aiohttp.ClientSession() as session:
									async with session.get('https://api.twitch.tv/kraken/streams/{}/?&client_id=4asyzu8i1l7ea1f61aebw3mgbuv04y2'.format(after.activity.url.replace('https://www.twitch.tv/', ''))) as r:
										tData = await r.json()
							except:
								pass
							embed = discord.Embed()
							embed.color = 0x593690
							embed.set_author(name=str(after), icon_url=after.avatar_url)
							embed.set_thumbnail(url=after.avatar_url)
							embed.title = after.activity.url
							embed.url = after.activity.url
							try:
								embed.description = "**{}** has started streaming **{}** and they're playing **{}**\n[Come watch them!]({})".format(str(after), after.activity.name, tData['stream']['game'], after.activity.url)
							except:
								embed.description = "**{}** has started streaming **{}** and they're playing **{}**\n[Come watch them!]({})".format(str(after), after.activity.name, "Unknown", after.activity.url)
							if after.guild.id == 106293726271246336:
								try:
									embed.set_thumbnail(url=tData['stream']['channel']['logo'])
								except:
									pass
								await self.bot.get_channel(after.guild.id).send(embed=embed)
							else:
								try:
									embed.set_image(url=tData['stream']['channel']['logo'])
								except:
									pass
								await self.bot.get_channel(109846625169453056).send(embed=embed)
							print('something happened with {} for stream'.format(after.id))

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.id != 175433427175211008 and before.guild.id == 91226580205961216:
			await self.DNstream(before, after)

def setup(bot):
	bot.add_cog(dragonnest(bot))
	bot.add_cog(streamer(bot))
