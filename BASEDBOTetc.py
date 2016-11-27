import requests
import json
import random
import re
import discord
from discord.ext import commands
import asyncio
import codecs

with open("C:/DISCORD BOT/Etc/malinfo.json") as j:
	malinfo = json.load(j)
with open("C:/DISCORD BOT/DiscordStuff/MainResponses.json") as j:
	MainResponses = json.load(j)
with open('C:/DISCORD BOT/BladeAndSoul/bnsemotes.txt') as inputF:
	bnsEmotes = inputF.read().splitlines()

unicodeResponses = {
	'!gardenintool':'(  ′︵‵  )/',
	"!donkmay":"🎊🚢💗 **DONMAYKAY**2⃣0⃣1⃣6⃣ 💗🚢🎊",
	"!oceanman":"OCEAN MAN 🌊 😍 Take me by the hand ✋ lead me to the land that you understand 🙌 🌊 OCEAN MAN 🌊 😍 The voyage 🚲 to the corner of the 🌎 globe is a real trip 👌 🌊 OCEAN MAN 🌊 😍 The crust of a tan man 👳 imbibed by the sand 👍 Soaking up the 💦 thirst of the land 💯"
}

class botetc:

	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def define(self, ctx):
		await self.bot.say(self.defines(ctx.message))

	def defines(self, message):
		if len(message.content.split()) == 1:
			return 'need something to define'
		words = message.content[8:]
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

	@commands.command(pass_context=True)
	async def mal(self, ctx):
		message = ctx.message
		if message.content.lower().split()[0] == '!mal' and len(message.content.split()) == 1:
			await self.bot.say('https://myanimelist.net/')
			return
		import xml.etree.ElementTree as ET
		anime = message.content.lower()[5:].replace(' ', '%20')
		r = requests.get('https://myanimelist.net/api/anime/search.xml?q=' + anime, auth=(malinfo['User Name'], malinfo['Password']))
		if 'cory in the house' in message.content.lower():
			embed = discord.Embed()
			embed.title = 'Cory in the House'
			embed.url = 'https://en.wikipedia.org/wiki/Cory_in_the_House'
			embed.color = 1983641
			embed.description="**Name: **{}\n**Status: **{}\n**Air Date: **{}\n**Episodes: **{}\n**Score: **{}\n**Description: **{}".format('コーリー ホワイトハウスでチョー大変! ','Finished','2007-01-12','34','10.00','Cory in the House is an American television series broadcast on the Disney Channel from 2007 to 2008 as a spin-off of the Disney series That’s So Raven, which focused on the exploits of the character Cory Baxter as he and his father take up residence in the White House. The series has since gained an ironic fandom online, including a running joke in which the series is erroneously referred to as an anime. Additionally, members of 4chan’s /v/ (video games) board have attempted to get the Cory in the House Nintendo DS game a most-wanted FAQ page on GameFAQs.')
			embed.set_image(url='http://img.lum.dolimg.com/v1/images/open-uri20150422-12561-zuhjen_2fc6aec3.jpeg?region=0%2C0%2C1000%2C1161')
			embed.set_footer(text='MyAnimeList', icon_url='http://i.imgur.com/8VjfkIQ.png')
			await self.bot.say(embed=embed)
			return
		if r.status_code == 200:
			ent=0
			if anime.lower().replace('%20', ' ') == 'orange':
				ent = 9
			resp = r.text
			tree = ET.fromstring(r.content)
			aUrl = 'https://myanimelist.net/anime/' + tree[ent][0].text
			try:
				aName = tree[ent][2].text
			except:
				aName = 'None'
			try:
				aJp = tree[ent][1].text
			except:
				aJp = 'None'
			aScore = tree[ent][5].text
			aEp = tree[ent][4].text
			aStat = tree[ent][7].text
			aDate = tree[ent][8].text
			aImg = tree[ent][-1].text
			try:
				aDesc = re.tree[ent][10].text.replace('&mdash;','—').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('<br />', '').replace('[i]', '').replace('[/i]', '')
			except:
				try:
					#root = ET.fromstring(resp)[0]
					aDesc = tree[ent][10].text.replace('&amp;','&').replace('&mdash;','—').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('<br />', '').replace('[i]', '').replace('[/i]', '')
				except:
					aDesc = 'None'

			embed = discord.Embed()
			embed.title = aName
			embed.url = aUrl
			embed.color = 1983641
			embed.description="**Name: **{}\n**Status: **{}\n**Air Date: **{}\n**Episodes: **{}\n**Score: **{}\n**Description: **{}".format(aJp,aStat,aDate,aEp,aScore,aDesc)
			embed.set_image(url=aImg)
			embed.set_footer(text='MyAnimeList', icon_url='http://i.imgur.com/8VjfkIQ.png')
			await self.bot.say(embed=embed)
		elif r.status_code == 204:
			await self.bot.say("I couldnt find an anime with that name in MyAnimeList")
		else:
			await self.bot.say("MyAnimeList is down, NOOOOOOOO :(")

	@commands.command(pass_context=True)
	async def checktwitch(self, ctx):
		await self.bot.say(self.checktw(ctx.message))

	def checktw(self, message):
		if len(message.content.split()) != 2:
			return 'The format of !checktwitch is `!checktwitch (channelname).`'
		tChan = message.content.split()[-1].lower()
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


	async def regions(self, message):
		for i in MainResponses["regions"]:
			for j in message.author.roles:
				if i in j.name and i.lower() == message.content.lower().replace('!', ''):
					await self.bot.remove_roles(message.author, discord.utils.get(message.server.roles, name = i))
					await asyncio.sleep(1)
					return
			if i.lower() == message.content.lower().replace('!', ''):
				await self.bot.add_roles(message.author, discord.utils.get(message.server.roles, name = i))
				await asyncio.sleep(1)
				return

	@commands.command(pass_context=True, no_pm=True)
	async def color(self, ctx):
		message = ctx.message
		if len(message.content.split()) == 1:
			await self.bot.say("Type in !colors or !colorlist so I can PM you a list of colors available, then type in `!color (nameofcolor)` for the color you want without the parentheses!")
			return
		rColor = message.content.lower().replace('!color ', '')
		currentcolor = ''
		requestedcolor = ''
		for i in MainResponses["colors"]:
			for j in message.author.roles:
				if i == j.name:
					currentcolor = j.name
			if i.lower() in rColor:
				requestedcolor = i
		if len(requestedcolor) == 0:
			await self.bot.say("Couldnt find that color! Make sure to copy the name from the list of colors!")
			return
		elif len(currentcolor) > 0 and len(requestedcolor) > 0:
			oldcolor = discord.utils.get(message.server.roles, name = currentcolor)
			newcolor = discord.utils.get(message.server.roles, name = requestedcolor)
			await self.bot.remove_roles(message.author, oldcolor)
			await asyncio.sleep(1)
			await self.bot.add_roles(message.author, newcolor)
			await self.bot.send_message(message.author, "I removed the {} color, and gave you the {} color!".format(currentcolor, requestedcolor))
		elif len(requestedcolor) > 0:
			newcolor = discord.utils.get(message.server.roles, name = requestedcolor)
			await self.bot.add_roles(message.author, newcolor)
			await self.bot.send_message(message.author, "I gave you the {} color!".format(requestedcolor))

	@commands.command(pass_context=True, aliases=['colorlist'], no_pm=True)
	async def colors(self, ctx):
		if ctx.message.server.id != '106293726271246336':
			return
		await self.bot.send_file(ctx.message.author, 'C:/DISCORD BOT/Etc/colorlist.png')
		return
	
	async def zealemotes(self, message):
		for i in message.content.lower().split():
			if i.startswith('!') and i.replace('!','') in bnsEmotes:
				await self.bot.send_file(message.channel, 'C:/DISCORD BOT/BladeAndSoul/bns_emotes/'+i.replace('!','')+'.png')
				return

	@commands.command()
	async def deleteian(self):
		with codecs.open('C:/DISCORD BOT/Etc/daddy.txt','r',"utf-8") as f:
			for i in f:
				await self.bot.say(i)
				await asyncio.sleep(2)


	async def bbresponse(self, message):
		if 'who are you' in message.content.lower():
			await self.bot.send_message(message.channel, 'I am a bot that runs on a community made python API(more info on that in bot-and-api channel) and programmed by Comphus to have functions for the Dragon Nest NA Community Discord Server')
			return
		if any(word in message.content.lower() for word in MainResponses['qQuestion']):
			await self.bot.send_message(message.channel, MainResponses['magicEight'][random.randint(0,19)]+', ' +  message.author.mention)
			return 
		elif 'hi' in message.content.lower() or 'hello' in message.content.lower():
			await self.bot.send_message(message.channel, 'Hi! ' + message.author.mention)
		elif 'bye' in message.content.lower():
			await self.bot.send_message(message.channel, 'Bye-Bye! ' + message.author.mention)
		elif 'i love you' in message.content.lower() or '<3' in message.content:
			await self.bot.send_message(message.channel, 'I love you too <3 ' + message.author.mention)
		elif 'thank' in message.content.lower():
			await self.bot.send_message(message.channel, 'You\'re welcome! ' + message.author.mention)
		elif 'fuck you' in message.content.lower() or 'fuck u' in message.content.lower() or '( ° ͜ʖ͡°)╭∩╮' in message.content:
			await self.bot.send_message(message.channel, '( ° ͜ʖ͡°)╭∩╮ ' + message.author.mention)
		else:
			await self.bot.send_message(message.channel, 'what? ' + message.author.mention)
		

	"""
	async def spookme(self):
		skeleR = random.randint(0,39)
		if skeleR <=30:
			await self.bot.send_message(self.message.channel, self.message.author.mention + ' YOU\'VE BEEN SPOOKED!')
			await self.bot.send_file(self.message.channel, 'C:/DISCORD BOT/Etc/spook_me/skele'+str(skeleR)+'.jpg')
		elif skeleR <=38:
			await self.bot.send_message(self.message.channel, self.message.author.mention + ' YOU\'VE BEEN SUPER SPOOKED!')
			await self.bot.send_file(self.message.channel, 'C:/DISCORD BOT/Etc/spook_me/skele'+str(skeleR)+'.jpg')
		else:
			await self.bot.send_message(self.message.channel, 'YOU\'VE BEEN SPOOKED TO DEATH\nhttps://www.youtube.com/watch?v=O8XfV8aPAyQ')
	"""

	@commands.command()
	async def lightproc(self):
		await self.bot.say('Buckle up!')
		await self.bot.upload('C:/DISCORD BOT/Etc/Comphus.jpg')

	async def mainprefixcommands(self, message):
		if message.content.lower().split()[0] in MainResponses['all!commands']:
			if message.content.lower().startswith(("!commands",'!help')):
				await self.bot.send_message(message.author, MainResponses['all!commands']['!commands'])
				await self.bot.send_message(message.author, MainResponses['all!commands']['!dncommands'])
				await self.bot.send_message(message.author, MainResponses['all!commands']['!bnscommands'])
				await self.bot.send_message(message.author, MainResponses['all!commands']['!games'])
				await self.bot.send_message(message.author, MainResponses['all!commands']['!dncdcommands'] + 'If you have any questions/requests, feel free to join the BASEDBOT server to ask!\nhttps://discord.gg/Gvt3Ks8')
			else:
				await self.bot.send_message(message.channel, MainResponses['all!commands'][message.content.lower().split()[0]])
		if message.channel.is_private == False and any(reg.lower() in message.content.lower() for reg in MainResponses["regions"]):
			await self.regions(message)

	async def on_message(self, message):
		if self.bot.user == message.author or message.channel.id == '168949939118800896' or message.author.id in '128044950024617984':
			return
		if message.content.startswith('!'):
			await self.mainprefixcommands(message)
		if '!' in message.content and message.channel.is_private == False and message.server.id not in '119222314964353025':
			await self.zealemotes(message)
		if message.content.startswith('<@175433427175211008>'):
			await self.bbresponse(message)
		if message.content in unicodeResponses:
			await self.bot.send_message(message.channel, unicodeResponses[message.content.lower().split()[0]])
		if message.content.startswith('!bruh') and message.channel.id != '106293726271246336':
			s = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 😂 👌'
			n = s.split()
			for i in range(15):
				r = random.randint(0, len(n)-1)
				await self.bot.add_reaction(message, n[r])


def setup(bot):
	bot.add_cog(botetc(bot))
