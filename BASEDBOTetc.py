import requests
import json
import random
import re
import discord
import asyncio
import codecs

with open("malinfo.json") as j:
	malinfo = json.load(j)
with open("MainResponses.json") as j:
	MainResponses = json.load(j)
with open('bnsemotes.txt') as inputF:
	bnsEmotes = inputF.read().splitlines()

unicodeResponses = {'/lenny':'( ͡° ͜ʖ ͡°)',
	'!gardenintool':'(  ′︵‵  )/',
	"!donkmay":"🎊🚢💗 **DONMAYKAY**2⃣0⃣1⃣6⃣ 💗🚢🎊",
	"!oceanman":"OCEAN MAN 🌊 😍 Take me by the hand ✋ lead me to the land that you understand 🙌 🌊 OCEAN MAN 🌊 😍 The voyage 🚲 to the corner of the 🌎 globe is a real trip 👌 🌊 OCEAN MAN 🌊 😍 The crust of a tan man 👳 imbibed by the sand 👍 Soaking up the 💦 thirst of the land 💯"
}

class botetc:

	def __init__(self, bot, message):
		self.bot = bot
		self.message = message

	def defines(self):
		if len(self.message.content.split()) == 1:
			return 'need something to define'
		words = self.message.content[8:]
		r = requests.get('http://api.urbandictionary.com/v0/define?term=' + words)
		tData = r.json()
		if r.status_code == 200:
			try:
				i = random.randint(0, len(tData['list'])-1)
				dWord = tData['list'][i]['word']
				dDef = tData['list'][i]['definition']
				dEx = tData['list'][i]['example']
				return "__Word__: {}\n__**Definition**__\n{}".format(dWord,dDef,dEx)
			except:
				return 'Word is not defined'
		else:
			return 'something went wrong :('

	def mal(self):
		if self.message.content.lower().split()[0] == '!mal' and len(self.message.content.split()) == 1:
			return 'https://myanimelist.net/'
		import xml.etree.ElementTree as ET
		anime = self.message.content.lower()[5:]
		r = requests.get('http://myanimelist.net/api/anime/search.xml?q=' + anime, auth=(malinfo['maluser'], malinfo['malpassword']))
		if r.status_code == 200:
			resp = r.text
			aUrl = 'http://myanimelist.net/anime/' + re.search("id>(\d+)</i", resp).group(1)
			try:
				aName = re.search("english>(\D+)</e", resp).group(1)
			except:
				aName = None
			try:
				aJp = re.search("title>(\D+)</t", resp).group(1)
			except:
				aJp = None
			aScore = re.search("score>(\S+|\s+)</s", resp).group(1)
			aEp = re.search("episodes>(\d+)</e", resp).group(1)
			aStat = re.search("status>(\D+)</s", resp).group(1)
			aDate = re.search("start_date>(\S+|\s+)</start_date", resp).group(1)
			try:
				aDesc = re.search("synopsis>(\S+|\s+)</synopsis", resp).group(1).replace('&mdash;','—').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('<br />', '').replace('[i]', '').replace('[/i]', '')
			except:
				try:
					root = ET.fromstring(resp)[0]
					aDesc = root[10].text.replace('&amp;','&').replace('&mdash;','—').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('<br />', '').replace('[i]', '').replace('[/i]', '')
				except:
					aDesc = None
			return "**Name: **{}\n**Eng Name: **{}\n**Status: **{}\n**Air Date: **{}\n**Episodes: **{}\n**Score: **{}\n**Description: **{}\n**Link: **{}".format(aJp,aName,aStat,aDate,aEp,aScore,aDesc,aUrl)
		elif r.status_code == 204:
			return "I couldnt find an anime with that name in MyAnimeList"
		else:
			return "MyAnimeList is down, NOOOOOOOO :("

	def checktwitch(self):
		if len(self.message.content.split()) != 2:
			return 'The format of !checktwitch is `!checktwitch (channelname).`'
		tChan = self.message.content.split()[-1].lower()
		r = requests.get('https://api.twitch.tv/kraken/streams/{}/?&client_id=4asyzu8i1l7ea1f61aebw3mgbuv04y2'.format(tChan))
		if r.status_code == 200:
			tData = r.json()
			if tData['stream'] == None:
				return tChan+'\'s channel is currently offline!'
			else:
				return tChan+'\'s channel is currently online!\n'+tChan+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+tChan)
		elif r.status_code == 404:
			return 'This channel does not exist.'
		elif r.status_code == 422:
			return 'Channel ' + tChan + ' is a justin.tv channel and doesnt work on twitch or is banned!'

	async def regions(self):
		for i in MainResponses["regions"]:
			for j in self.message.author.roles:
				if i in j.name and i.lower() == self.message.content.lower().replace('!', ''):
					await self.bot.remove_roles(self.message.author, discord.utils.get(self.message.server.roles, name = i))
					await asyncio.sleep(1)
					return
			if i.lower() == self.message.content.lower().replace('!', ''):
				await self.bot.add_roles(self.message.author, discord.utils.get(self.message.server.roles, name = i))
				await asyncio.sleep(1)
				return
	
	async def color(self):
		if len(self.message.content.split()) == 1:
			await self.bot.send_message(self.message.channel, "Type in !colors or !colorlist so I can PM you a list of colors available, then type in `!color (nameofcolor)` for the color you want without the parentheses!")
			return
		rColor = self.message.content.lower().replace('!color ', '')
		currentcolor = ''
		requestedcolor = ''
		for i in MainResponses["colors"]:
			for j in self.message.author.roles:
				if i == j.name:
					currentcolor = j.name
			if i.lower() in rColor:
				requestedcolor = i
		if len(requestedcolor) == 0:
			await self.bot.send_message(self.message.channel, "Couldnt find that color! Make sure to copy the name from the list of colors!")
			return
		elif len(currentcolor) > 0 and len(requestedcolor) > 0:
			oldcolor = discord.utils.get(self.message.server.roles, name = currentcolor)
			newcolor = discord.utils.get(self.message.server.roles, name = requestedcolor)
			await self.bot.remove_roles(self.message.author, oldcolor)
			await asyncio.sleep(1)
			await self.bot.add_roles(self.message.author, newcolor)
			await self.bot.send_message(self.message.author, "I removed the {} color, and gave you the {} color!".format(currentcolor, requestedcolor))
		elif len(requestedcolor) > 0:
			newcolor = discord.utils.get(self.message.server.roles, name = requestedcolor)
			await self.bot.add_roles(self.message.author, newcolor)
			await self.bot.send_message(self.message.author, "I gave you the {} color!".format(requestedcolor))

	async def colors(self):
		await self.bot.send_file(self.message.author, 'colorlist.png')
		return
	
	async def zealemotes(self):
		for i in self.message.content.lower().split():
			if i.startswith('!') and i.replace('!','') in bnsEmotes:
				await self.bot.send_file(self.message.channel, 'C:/DISCORD BOT/bns_emotes/'+i.replace('!','')+'.png')
				return
	async def deleteian(self):
		with codecs.open('daddy.txt','r',"utf-8") as f:
			for i in f:
				await self.bot.send_message(self.message.channel, i)
				await asyncio.sleep(2)

	async def bbresponse(self):
		if 'who are you' in self.message.content.lower():
			await self.bot.send_message(self.message.channel, 'I am a bot that runs on a community made python API(more info on that in bot-and-api channel) and programmed by Comphus to have functions for the Dragon Nest NA Community Discord Server')
			return
		if any(word in self.message.content.lower() for word in MainResponses['qQuestion']):
			await self.bot.send_message(self.message.channel, MainResponses['magicEight'][random.randint(0,19)]+', ' +  self.message.author.mention)
			return 
		elif 'hi' in self.message.content.lower() or 'hello' in self.message.content.lower():
			await self.bot.send_message(self.message.channel, 'Hi! ' + self.message.author.mention)
		elif 'bye' in self.message.content.lower():
			await self.bot.send_message(self.message.channel, 'Bye-Bye! ' + self.message.author.mention)
		elif 'i love you' in self.message.content.lower() or '<3' in self.message.content:
			await self.bot.send_message(self.message.channel, 'I love you too <3 ' + self.message.author.mention)
		elif 'thank' in self.message.content.lower():
			await self.bot.send_message(self.message.channel, 'You\'re welcome! ' + self.message.author.mention)
		elif 'fuck you' in self.message.content.lower() or 'fuck u' in self.message.content.lower() or '( ° ͜ʖ͡°)╭∩╮' in self.message.content:
			await self.bot.send_message(self.message.channel, '( ° ͜ʖ͡°)╭∩╮ ' + self.message.author.mention)
		else:
			await self.bot.send_message(self.message.channel, 'what? ' + self.message.author.mention)

	async def spookme(self):
		skeleR = random.randint(0,39)
		if skeleR <=30:
			await self.bot.send_message(self.message.channel, self.message.author.mention + ' YOU\'VE BEEN SPOOKED!')
			await self.bot.send_file(self.message.channel, 'skele'+str(skeleR)+'.jpg')
		elif skeleR <=38:
			await self.bot.send_message(self.message.channel, self.message.author.mention + ' YOU\'VE BEEN SUPER SPOOKED!')
			await self.bot.send_file(self.message.channel, 'skele'+str(skeleR)+'.jpg')
		else:
			await self.bot.send_message(self.message.channel, 'YOU\'VE BEEN SPOOKED TO DEATH\nhttps://www.youtube.com/watch?v=O8XfV8aPAyQ')

	async def lightproc(self):
		await self.bot.send_message(self.message.channel, 'Buckle up!')
		await self.bot.send_file(self.message.channel, 'Comphus.jpg')

	async def mainprefixcommands(self):
		if self.message.content.lower().split()[0] in MainResponses['all!commands']:
			if self.message.content.lower().startswith("!commands"):
				await self.bot.send_message(self.message.author, MainResponses['all!commands'][self.message.content.lower().split()[0]])
				await self.bot.send_message(self.message.author, MainResponses['all!commands']['!dncommands'])
				await self.bot.send_message(self.message.author, MainResponses['all!commands']['!bnscommands'])
				await self.bot.send_message(self.message.author, MainResponses['all!commands']['!games'])
				await self.bot.send_message(self.message.author, MainResponses['all!commands']['!dncdcommands'])
			else:
				await self.bot.send_message(self.message.channel, MainResponses['all!commands'][self.message.content.lower().split()[0]])
		if any(reg.lower() in self.message.content.lower() for reg in MainResponses["regions"]):
			await self.regions()
	async def cats(self):
		rcats = random.choice(os.listdir("C:/DISCORD BOT/cats"))
		await self.bot.send_file(self.message.channel, 'C:/DISCORD BOT/cats/'+rcats)
