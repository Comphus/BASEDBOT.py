import requests
import discord
from discord.ext import commands

class bladeandsoul:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def bns(self, ctx):
		message = ctx.message
		if len(message.content.split()) == 1:
			await self.bot.say('the format for seeing a players bns info is \'!bns (player ign)\'')
			return
		newerM = message.content.lower()[5:].split()
		if len(newerM) > 1:
			newestM = '%20'.join(newerM)
		else:
			newestM = newerM[0]
		if "faggot" in newestM.lower():
			await self.bot.say('http://na-bns.ncsoft.com/ingame/bs/character/profile?c=Rain\nhttp://na-bns.ncsoft.com/ingame/bs/character/profile?c=Minko')
		r = requests.get('http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+newestM)
		if len(r.history) == 0:
			finalmessage = 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c={}&s=101'.format(newestM)
			from bs4 import BeautifulSoup
			soup = BeautifulSoup(r.text, 'html.parser')
			#print(soup.find_all("div", class_="charaterView")[0].img['src'])
			#print(soup.find_all(attrs={"class":"signature"})[0].find_all(attrs={"href":"#"})[0].string)#.find_all(attrs={"class":"desc"})[0])
			try:
				clan = soup.find_all(attrs={"class":"signature"})[0].find_all(attrs={"class":"guild"})[0].text
			except:
				clan = 'None'
			classname = soup.find_all(attrs={"class":"signature"})[0].find_all("ul")[0].li.string
			level = soup.find_all(attrs={"class":"signature"})[0].find_all("li")[1].text.split()[1]
			try:
				hmlevel = soup.find_all(attrs={"class":"signature"})[0].find_all("li")[1].find_all(attrs={"class":"masteryLv"})[0].string.replace("Hongmoon Level", "**Hongmoon Level:**")
			except:
				hmlevel = "**Dark Arts Level:** 0"
			classicon = soup.find_all("div", class_="classThumb")[0].img['src']
			#accname = soup.find_all("a", href="#")[0].string
			name = soup.find_all("span", attrs={'class':"name"})[0].string
			att = soup.find_all("div", class_="attack")[0].span.string
			hp = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[0].find(class_="stat-point").string
			pierce = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-title"})[2].find(class_="stat-point").string
			piercep = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-description"})[2].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			defense = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[1].find(class_="stat-point").string
			defensep = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-description"})[1].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			acc = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-title"})[3].find(class_="stat-point").string
			accp = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-description"})[3].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			eva = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[3].find(class_="stat-point").string
			evap = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-description"})[3].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			chit = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-title"})[5].find(class_="stat-point").string
			chitp = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-description"})[5].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			block = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[4].find(class_="stat-point").string
			blockp = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-description"})[4].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[4].string
			cdmg = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-title"})[6].find(class_="stat-point").string
			cdmgp = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-description"})[6].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			critd = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[5].find(class_="stat-point").string
			critdp = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-description"})[5].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[1].string
			finalmessage += "\n**Clan:** {}\n**Class:** {}\n**Level:** {}\n{}\n**Attack:** {}                                                        **HP:** {}\n**Pierce:** {}({})                                          **Defense:** {}({})\n**Accuracy:** {}({})                                 **Evasion:** {}({})\n**Critical Hit:** {}({})                              **Block:** {}({})\n**Critical Damage** {}({})                    **Crit Defense:** {}({})\n".format(clan,classname,level,hmlevel,att,hp,pierce,piercep,defense,defensep,acc,accp,eva,evap,chit,chitp,block,blockp,cdmg,cdmgp,critd,critdp)
			try:
				finalmessage += soup.find_all("div", class_="charaterView")[0].img['src']
			except:
				pass


			lft = "**Attack:** {}\n**Pierce:** {}({})\n**Accuracy:** {}({})\n**Critical Hit:** {}({})\n**Critical Damage** {}({})".format(att,pierce,piercep,acc,accp,chit,chitp,cdmg,cdmgp)
			rgt = "**HP:** {}\n**Defense:** {}({})\n**Evasion:** {}({})\n**Block:** {}({})\n**Crit Defense:** {}({})\n".format(hp,defense,defensep,eva,evap,block,blockp,critd,critdp)

			embed = discord.Embed()
			embed.set_author(name=classname, icon_url=classicon)
			embed.title = name.replace('[','').replace(']','')
			embed.url = 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+newestM
			if classname == 'Blade Master':
				embed.color = 16718105
			if classname == 'Kung Fu Master':
				embed.color = 3325695
			if classname == 'Assassin':
				embed.color = 2123412
			if classname == 'Destroyer':
				embed.color = 10038562
			if classname == 'Blade Dancer':
				embed.color = 7419530
			if classname == 'Soul Fighter':
				embed.color = 3066993
			if classname == 'Warlock':
				embed.color = 15620599
			if classname == 'Force Master':
				embed.color = 15105570
			if classname == 'Summoner':
				embed.color = 15844367
			embed.add_field(name="__General Info__", value="**Clan:** {}\n**Level:** {}\n{}".format(clan,level,hmlevel), inline = False)
			embed.add_field(name="__Offensive__", value=lft)
			embed.add_field(name="__Defensive__", value=rgt)
			embed.set_image(url=soup.find_all("div", class_="charaterView")[0].img['src'])
			embed.set_footer(text='Blade and Soul', icon_url='http://i.imgur.com/a1kk9Tq.png')
			

			await self.bot.say(embed=embed)
		else:
			await self.bot.say('Character name does not exist')

	@commands.command(pass_context=True)
	async def bnstree(self, ctx):
		await self.bot.say(self.bnst(ctx.message))

	def bnst(self, message):
		bnsClass = message.content.replace('!bnstree ', '').lower()
		if '!bnstree' == message.content:
			return 'https://bnstree.com/'
		elif 'blade master' == bnsClass or 'bm' == bnsClass:
			return 'https://bnstree.com/tree/BM'
		elif 'kfm' == bnsClass or 'kungfu master' == bnsClass or 'kung fu master' == bnsClass or 'kungfumaster' == bnsClass or 'kf' == bnsClass:
			return 'https://bnstree.com/tree/KF'
		elif 'destroyer' == bnsClass or 'des' == bnsClass or 'de' == bnsClass or 'destro' == bnsClass or 'dest' == bnsClass:
			return 'https://bnstree.com/tree/DE'
		elif 'force master' == bnsClass or 'fm' == bnsClass or 'forcemaster' == bnsClass or 'force user' == bnsClass:
			return 'https://bnstree.com/tree/FM'
		elif 'assassin' == bnsClass or 'as' == bnsClass or 'sin' == bnsClass:
			return 'https://bnstree.com/tree/AS'
		elif 'summoner' == bnsClass or 'su' == bnsClass or 'summ' == bnsClass or 'sum' == bnsClass:
			return 'https://bnstree.com/tree/SU'
		elif 'blade dancer' == bnsClass or 'bd' == bnsClass or 'bladedancer' == bnsClass or 'lbm' == bnsClass or 'lyn blade master' == bnsClass or 'lynblade master' == bnsClass or 'lyn blademaster' == bnsClass:
			return 'https://bnstree.com/tree/BD'
		elif 'warlock' == bnsClass or 'wl' == bnsClass or 'lock' == bnsClass:
			return 'https://bnstree.com/tree/WL'
		elif 'soul fighter' == bnsClass or 'sf' == bnsClass or 'soulfighter' in bnsClass or 'chi master' in bnsClass or 'chimaster' in bnsClass:
			return 'https://bnstree.com/tree/SF'
		else:
			return '2nd argument not recognised'


	"""will be rebuilt when i think of something new for it since it hasnt been used in a LONG time
	def savebnsbuild(self):
		if self.message.content == ('!savebnsbuild') or self.message.content == ('!savebnsbuild '):
			return 'Your build must contain the format (!savebnsbuild !!(name of command) (tree build url)'
		elif self.message.content.split()[-1].startswith('https://bnstree.com/') == False:
			return 'Your URL must be from bnstree.com or is missing the https:// prefix'
		elif self.message.content.split()[1].startswith('!!') == False:
			return 'Your command created command must have !! infront'
		elif len(self.message.content.split()) !=3:
			return 'Can only create a link with exactly 3 arguments'
		elif len(self.message.content.split()) == 3 and '!!' in self.message.content.split()[1]: 
			with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt','r+') as bnsBuilds:
				for line in bnsBuilds:
					if self.message.content.split()[1] in line:
						return 'A build with this name already exists!'
		bnsBuildsSave = self.message.content.replace('!savebnsbuild ', '')
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt','a') as bnsBuilds2:
			bnsBuilds2.write(str(self.message.author.id) + ' ' + bnsBuildsSave + '\n')
			return 'build "'+self.message.content.split()[2]+'" saved! Use your command "'+self.message.content.split()[1]+'" to use it!'


	def editbnsbuild(self):
		if self.message.content == ('!editbnsbuild') or self.message.content == ('!editbnsbuild '):
			return 'Your build must contain the format !editbnsbuild !!(name of command) (tree build url)'
		elif self.message.content.split()[-1].startswith('https://bnstree.com/') == False:
			return 'Your URL must be from bnstree.com or is missing the https:// prefix'
		if self.message.content.split()[1].startswith('!!') == False:
			return 'Your edited command must have !! infront'
		if len(str(self.message.content).split()) !=3:
			return 'Can only edit a link with exactly 3 arguments'
		saveL = ''
		dnBuildsSave = self.message.content.replace('!editbnsbuild ', '')
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt','r') as bnsBuilds2:
			for line in bnsBuilds2:
				if self.message.content.split()[1] in line:
					if str(self.message.author.id) not in line:
						return 'This is not your build so you cannot edit it.'
					elif str(self.message.author.id) in line:
						saveL = line.rsplit(' ', 1)[0] + ' ' + self.message.content.split()[-1]
		saveL += '\n'
		newLines = []
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt','r') as bnsBuilds2:
			for line in bnsBuilds2:
				if self.message.content.split()[1] not in line:
					newLines.append(line)
				else:
					newLines.append(saveL)
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt','w') as bnsBuilds2:
			for line in newLines:
				bnsBuilds2.write(line)
		return 'build "'+self.message.content.split()[2]+'" has been edited! Use your command "'+self.message.content.split()[1]+'" to use it!'

	def deletebnsbuild(self):
		if self.message.content == ('!deletebnsbuild') or self.message.content == ('!deletebnsbuild '):
			return 'Your build must contain the format !deletebnsbuild !!(name of command)'
		elif self.message.content.split()[1].startswith('!!') == False:
			return 'Your command created command must have !! infront'
		elif len(str(self.message.content).split()) !=2:
			return 'Can only delete a link with exactly 2 arguments'
		dnBuildsSave = self.message.content.replace('!deletebnsbuild ', '')
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt','r') as bnsBuilds2:
			for line in bnsBuilds2:
				if self.message.content.split()[1] in line:
					if str(self.message.author.id) not in line:
						return 'This is not your build so you cannot delete it.'
		newLines = []
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt','r') as bnsBuilds2:
			for line in bnsBuilds2:
				if self.message.content.split()[1] not in line:
					newLines.append(line)
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt','w') as bnsBuilds2:
			for line in newLines:
				bnsBuilds2.write(line)
		return 'Your build ' + self.message.content.split()[-1] + ' has been deleted.'
	



	def prefixbns(self, message): # for the !! prefix
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt') as readBuilds:
			for line in readBuilds:
				if message.content.split()[0] == line.split()[1]:
					return line.split()[-1]

	
	async def prefixbnscommands(self):
		if self.prefixbns() == None:
			return
		else:
			await self.bot.send_message(self.message.channel, self.prefixbns())
	

	def mybns(self, message):
		numbercount = 1
		returnbox = []
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt') as readBuilds:
			for line in readBuilds:
				if str(message.author.id) in line:
					returnbox.append(str(numbercount)+': '+line.replace(str(message.author.id)+ ' ', ''))
					numbercount += 1
		if len(returnbox) == 0:
			return ['You have no saved builds!']
		else:
			return returnbox


	@commands.command(pass_context=True)
	async def mybnsbuilds(self, ctx):
		for line in self.mybns(ctx.message):
			await self.bot.say(line)
	"""

	@commands.command(pass_context=True)
	async def bnsmarket(self, ctx):#whenever i get back from school tomorrow make it so it searches instead of exact
		message = ctx.message
		if len(message.content.split()) == 1:
			await self.bot.send_message(message.channel, "In order to use the BNS market search function, type in whatever item after you type `!bnsmarket` so i can search through <http://www.bnsmarketplace.com/search> for it. Currently i only look for the item exactly as typed, will be upgraded later!")
			return
		m = message.content.lower().replace('!bnsmarket ', '').replace(' ', '_')
		from bs4 import BeautifulSoup
		r = requests.get('http://www.bnsmarketplace.com/search/{}'.format(m))
		soup = BeautifulSoup(r.text, 'html.parser')
		try:
			NAg = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNAGold"})[0].string
		except:
			t = requests.get('http://www.bnsmarketplace.com/item/{}'.format(m))
			soups = BeautifulSoup(t.text, 'html.parser')
			try:
				err = soups.find_all(attrs={"id":"textResult"})[0].string
				if err is None:
					pass
				else:
					top5 = 'Sorry, I cant find exactly what {} is, here are the top results(up to 5) for it:```xl\n'.format(m)
					try:
						res = soup.find_all(attrs={"id":"main"})[0].find_all(attrs={"id":"repeaterResult_itemContainer_0"})[0].string
					except:
						await self.bot.say("Sorry, I couldnt find any item relating to `{}`.".format(m))
						return
					for i in range(5):
						try:
							res = soup.find_all(attrs={"id":"main"})[0].find_all(attrs={"id":"repeaterResult_textItemName_{}".format(i)})[0].string
							top5 += '{}\n'.format(res)
						except:
							pass
					top5 += '```'
					await self.bot.say(top5)
					return
			except:
				pass
		r = requests.get('http://www.bnsmarketplace.com/item/{}'.format(m))
		soup = BeautifulSoup(r.text, 'html.parser')

		NAg = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNAGold"})[0].string
		NAs = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNASilver"})[0].string
		NAc = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNACopper"})[0].string
		NAu = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNAUpdated"})[0].string

		EUg = soup.find_all(attrs={"id":"EUPanel"})[0].find_all(attrs={"id":"priceEUGold"})[0].string
		EUs = soup.find_all(attrs={"id":"EUPanel"})[0].find_all(attrs={"id":"priceEUSilver"})[0].string
		EUc = soup.find_all(attrs={"id":"EUPanel"})[0].find_all(attrs={"id":"priceEUCopper"})[0].string
		EUu = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNAUpdated"})[0].string

		await self.bot.say("**__NA:__**\n<:VipGold:248714191517646848>** {} **<:VipSilver:248714227877937152>** {}  **<:VipBronze:248714357792440320>** {}** `{}`\n**__EU:__**\n<:VipGold:248714191517646848>** {} **<:VipSilver:248714227877937152>** {}  **<:VipBronze:248714357792440320>** {}** `{}`".format(NAg,NAs,NAc,NAu,EUg,EUs,EUc,EUu))


	@commands.command()
	async def mspguide(self):
		await self.bot.say('https://drive.google.com/file/d/0Bx5A-bjrg1p1aVlJZElJV3JoWk0/view')


def setup(bot):
	bot.add_cog(bladeandsoul(bot))
