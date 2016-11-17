import requests

class bladeandsoul:

	def __init__(self, bot, message):
		self.bot = bot
		self.message = message


	def bnssearch(self):
		if len(self.message.content.split()) == 1:
			return 'the format for seeing a players bns info is \'!bns (player ign)\''
		newerM = self.message.content.lower()[5:].split()
		if len(newerM) > 1:
			newestM = '%20'.join(newerM)
		else:
			newestM = newerM[0]
		if "faggot" in newestM.lower():
			return 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c=Rain\nhttp://na-bns.ncsoft.com/ingame/bs/character/profile?c=Minko'
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
			return finalmessage
		else:
			return 'Character name does not exist'

	def bnstree(self):
		bnsClass = self.message.content.replace('!bnstree ', '').lower()
		if '!bnstree' == self.message.content:
			return 'https://bnstree.com/'
		elif 'blade master' == bnsClass or 'bm' == bnsClass:
			return 'https://bnstree.com/BM'
		elif 'kfm' == bnsClass or 'kungfu master' == bnsClass or 'kung fu master' == bnsClass or 'kungfumaster' == bnsClass or 'kf' == bnsClass:
			return 'https://bnstree.com/KF'
		elif 'destroyer' == bnsClass or 'des' == bnsClass or 'de' == bnsClass or 'destro' == bnsClass or 'dest' == bnsClass:
			return 'https://bnstree.com/DE'
		elif 'force master' == bnsClass or 'fm' == bnsClass or 'forcemaster' == bnsClass or 'force user' == bnsClass:
			return 'https://bnstree.com/FM'
		elif 'assassin' == bnsClass or 'as' == bnsClass or 'sin' == bnsClass:
			return 'https://bnstree.com/AS'
		elif 'summoner' == bnsClass or 'su' == bnsClass or 'summ' == bnsClass or 'sum' == bnsClass:
			return 'https://bnstree.com/SU'
		elif 'blade dancer' == bnsClass or 'bd' == bnsClass or 'bladedancer' == bnsClass or 'lbm' == bnsClass or 'lyn blade master' == bnsClass or 'lynblade master' == bnsClass or 'lyn blademaster' == bnsClass:
			return 'https://bnstree.com/BD'
		elif 'warlock' == bnsClass or 'wl' == bnsClass or 'lock' == bnsClass:
			return 'https://bnstree.com/WL'
		elif 'soul fighter' == bnsClass or 'sf' == bnsClass or 'soulfighter' in bnsClass or 'chi master' in bnsClass or 'chimaster' in bnsClass:
			return 'https://bnstree.com/SF'
		else:
			return '2nd argument not recognised'

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



	def prefixbns(self): # for the !! prefix
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt') as readBuilds:
			for line in readBuilds:
				if self.message.content.split()[0] == line.split()[1]:
					return line.split()[-1]

	async def prefixbnscommands(self):
		if self.prefixbns() == None:
			return
		else:
			await self.bot.send_message(self.message.channel, self.prefixbns())

	def mybns(self):
		numbercount = 1
		returnbox = []
		with open('C:/DISCORD BOT/BladeAndSoul/BNSbuilds.txt') as readBuilds:
			for line in readBuilds:
				if str(self.message.author.id) in line:
					returnbox.append(str(numbercount)+': '+line.replace(str(self.message.author.id)+ ' ', ''))
					numbercount += 1
		if len(returnbox) == 0:
			return ['You have no saved builds!']
		else:
			return returnbox

	async def mybnsbuilds(self):
		for line in self.mybns():
			await self.bot.send_message(self.message.channel, line)

	async def bnsmarket(self):#whenever i get back from school tomorrow make it so it searches instead of exact
		if len(self.message.content.split()) == 1:
			await self.bot.send_message(self.message.channel, "In order to use the BNS market search function, type in whatever item after you type `!bnsmarket` so i can search through <http://www.bnsmarketplace.com/search> for it. Currently i only look for the item exactly as typed, will be upgraded later!")
			return
		m = self.message.content.lower().replace('!bnsmarket ', '').replace(' ', '_')
		r = requests.get('http://www.bnsmarketplace.com/item/{}'.format(m))
		from bs4 import BeautifulSoup
		soup = BeautifulSoup(r.text, 'html.parser')
		err = soup.find_all(attrs={"id":"textResult"})[0].string
		try:
			if len(err) > 0:
				await self.bot.send_message(self.message.channel, "Sorry, I could not find that item!")
				return
		except:
			pass
		NAg = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNAGold"})[0].string
		NAs = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNASilver"})[0].string
		NAc = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNACopper"})[0].string
		NAu = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNAUpdated"})[0].string

		EUg = soup.find_all(attrs={"id":"EUPanel"})[0].find_all(attrs={"id":"priceEUGold"})[0].string
		EUs = soup.find_all(attrs={"id":"EUPanel"})[0].find_all(attrs={"id":"priceEUSilver"})[0].string
		EUc = soup.find_all(attrs={"id":"EUPanel"})[0].find_all(attrs={"id":"priceEUCopper"})[0].string
		EUu = soup.find_all(attrs={"id":"NAPanel"})[0].find_all(attrs={"id":"priceNAUpdated"})[0].string

		await self.bot.send_message(self.message.channel, "**__NA:__**\n<:VipGold:248714191517646848>** {} **<:VipSilver:248714227877937152>** {}  **<:VipBronze:248714357792440320>** {}** `{}`\n**__EU:__**\n<:VipGold:248714191517646848>** {} **<:VipSilver:248714227877937152>** {}  **<:VipBronze:248714357792440320>** {}** `{}`".format(NAg,NAs,NAc,NAu,EUg,EUs,EUc,EUu))

