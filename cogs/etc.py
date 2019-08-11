import aiohttp
import json
import random
import re
import discord
from discord.ext import commands
from .utils import checks
import asyncio
import codecs

with open("C:/DISCORD BOT/Etc/malinfo.json") as j:
	malinfo = json.load(j)
with open("C:/DISCORD BOT/DiscordStuff/MainResponses.json") as j:
	MainResponses = json.load(j)
with open('C:/DISCORD BOT/BladeAndSoul/bnsemotes.txt') as inputF:
	bnsEmotes = inputF.read().splitlines()

enhancing = {}
unicodeResponses = {
	'/lenny':'( ͡° ͜ʖ ͡°)',
	'gardenintool':'(  ′︵‵  )/',
	"donkmay":"🎊🚢💗 **DONMAYKAY**2⃣0⃣1⃣6⃣ 💗🚢🎊",
	"oceanman":"OCEAN MAN 🌊 😍 Take me by the hand ✋ lead me to the land that you understand 🙌 🌊 OCEAN MAN 🌊 😍 The voyage 🚲 to the corner of the 🌎 globe is a real trip 👌 🌊 OCEAN MAN 🌊 😍 The crust of a tan man 👳 imbibed by the sand 👍 Soaking up the 💦 thirst of the land 💯"
}
boxkurtz = {}

class botetc(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.enhancefee = {#put this and ment in MainResponses
		# dz cost aeth  wc ae up-chn brk
		0:[126429, 2618, 0, 8, 10000, 0, 100, 0],
		1:[126429, 2618, 0, 8, 10000, 0, 100, 1],
		2:[126429, 2618, 0, 8, 10000, 0, 100, 1],
		3:[126429, 3927, 0, 8, 3500, 0, 100, 1],
		4:[126429, 3927, 0, 8, 2500, 1000, 1],
		5:[126429, 3927, 0, 8, 1500, 2500, 100, 1],
		6:[126429, 3927, 3, 8, 500, 4000, 100, 1],
		7:[126429, 3927, 3, 8, 200, 5500, 100, 1],
		8:[126429, 3927, 3, 8, 25, 7500, 100, 1]
		}

	async def emojihance(self, ctx, message, m):
		await m.remove_reaction("🔨", message.author)
		dotdot = [".",". .",". . ."]
		for i in range(3):
			await m.edit(content="Enhancing your LV55 Unique-Grade weapon **{}**".format(dotdot[i]))
			await asyncio.sleep(.7)
		results = await self.enhancewep(ctx, message, m)
		await m.edit(content=results)
		if enhancing[message.author.id][0] == 9:
			await ctx.send("Your weapon is +9, you won the game. Resetting progress!")
			enhancing[message.author.id] = [0, 0, 0, 0, 0, 0, 0, message]
			return
		def pred(r, mess):
				return mess == message.author and r.emoji == "🔨" and r.message.id == m.id
		try:
			user, rec = await self.bot.wait_for('reaction_add', check=pred, timeout=60)
		except asyncio.TimeoutError:
			#await ctx.send("reaction timed out!")
			await m.remove_reaction("🔨", self.bot.user)
			return
		else:
			await self.emojihance(ctx, message, m)

	@commands.command(aliases=["swenh","swe"])
	#@checks.not_lounge()
	async def swenhance(self, ctx):
		message = ctx.message
		if 'stop' in message.content.lower():
			await ctx.send("I have reset your enhancing progress")
			enhancing[message.author.id] = [0, 0, 0, 0, 0, 0, 0, message]
			#					       	level dz aeth ae wc anti-des
			return
		if message.author.id not in enhancing:
			enhancing[message.author.id] = [0, 0, 0, 0, 0, 0, 0, message]
		if message.author.id in enhancing:
			dotdot = [". .",". . ."]
			m = await ctx.send("Enhancing your LV55 Unique-Grade weapon **.**")
			await asyncio.sleep(.7)
			for i in range(2):
				await m.edit(content="Enhancing your LV55 Unique-Grade weapon **{}**".format(dotdot[i]))
				await asyncio.sleep(.7)
			if message.content.split()[-1] in ["+4","+5","+6","+7","+8","+9"]:
				enhances = {"+4":4,"+5":5,"+6":6,"+7":7,"+8":8,"+9":9}
				enhancing[message.author.id] = [0, 0, 0, 0, 0, 0, 0, message]
				s = enhances.get(message.content.split()[-1])
				if s is None:
					await ctx.send("can only input either +6, +7, +8 or +9")
					return
				while True:
					results = await self.enhancewep(ctx, message, m)
					if enhancing[message.author.id][0] >= s:
						expns = enhancing[message.author.id][6] -25
						if expns <= 0:
							expns = 0
						else:
							expns = int(expns/5) +1
						ss = "Enhancement __**Successful!**__\nYour 55 Weapon is now: **+{}**\nYou have spent a total of: \n**{:,.2f}** DZ   **{}** <:aethar:435208496510926878> \n**{}** <:normalaetharite:435208601389367297>    **{}** <:weaponupchip:435208556904579093>    **{}** <:antidestruct:435208503880187924>    **{}** <:strengthexpansion:435973634977431553>\n__**{}**__/25 attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], enhancing[message.author.id][2], enhancing[message.author.id][3], enhancing[message.author.id][4], enhancing[message.author.id][5], expns,enhancing[message.author.id][6])
						await ctx.send("results are: @ {}\n{}".format(str(message.author), ss))
						AeP = enhancing[message.author.id][3] * 90000
						WucP = enhancing[message.author.id][4] * 30000000
						AdP = enhancing[message.author.id][5] * 100000000
						SeP = expns * 700000000
						TotalP = enhancing[message.author.id][1] + AeP + WucP + AdP + SeP
						mmoahP = TotalP/200000000*1.00
						await ctx.send("Total amount of DZ spent(based on market prices for everything)\n{:,.2f} DZ+\n<:normalaetharite:435208601389367297> {:,.2f} +\n<:weaponupchip:435208556904579093> {:,.2f} +\n<:antidestruct:435208503880187924> {:,.2f} +\n__<:strengthexpansion:435973634977431553> {:,.2f} =__\n**{:,.2f} DZ** ≅ **${:,.2f}** at <https://www.mmoah.com/soul-worker>".format(enhancing[message.author.id][1], AeP, WucP, AdP, SeP, TotalP, mmoahP))
						enhancing[message.author.id] = [0, 0, 0, 0, 0, 0, 0, message]
						return
			if enhancing[message.author.id][0] == 9:
				await ctx.send("Your weapon is +9, you won the game. Resetting progress!")
				enhancing[message.author.id] = [0, 0, 0, 0, 0, 0, 0, message]
				return
			results = await self.enhancewep(ctx, message, m)
			await m.edit(content=results)
			await m.add_reaction("🔨")
			def pred(r, mess):
				return mess == message.author and r.emoji == "🔨" and r.message.id == m.id
			try:
				user, rec = await self.bot.wait_for('reaction_add', check=pred, timeout=60)
			except asyncio.TimeoutError:
				#await ctx.send("reaction timed out!")
				await m.remove_reaction("🔨", self.bot.user)
				return
			else:
				await self.emojihance(ctx, message, m)

	async def enhancewep(self, ctx, message, m):
		tryagain = True
		while tryagain:#just a var to name what the enhance thingy does, can just write True
			a = random.randint(1, 10000) #the succ, if no succ then fails
			b = random.randint(1, 10000) #break rate to implement
			d = random.randint(1, 10000)
			try:
				if a <= self.enhancefee[enhancing[message.author.id][0]][4]:
					if enhancing[message.author.id][0] >= 4:
						enhancing[message.author.id][5] += 1#anti destructions
					enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]#dz
					enhancing[message.author.id][2] += self.enhancefee[enhancing[message.author.id][0]][1]#aetharite
					enhancing[message.author.id][3] += self.enhancefee[enhancing[message.author.id][0]][3]#normal aetharite
					enhancing[message.author.id][4] += self.enhancefee[enhancing[message.author.id][0]][2]#weapon upgrade chips
					enhancing[message.author.id][6] += 1#number of attempts
					enhancing[message.author.id][0] += 1#enhance increase

					#await m.edit(content="Enhancement __**Successful!**__\nYour 55 Weapon is now: **+{}**\nYou have spent a total of: \n**{:,.2f}** DZ   **{}** <:aethar:435208496510926878> \n**{}** <:normalaetharite:435208601389367297>    **{}** <:weaponupchip:435208556904579093>    **{}** <:antidestruct:435208503880187924>\n__**{}**__/25 attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], enhancing[message.author.id][2], enhancing[message.author.id][3], enhancing[message.author.id][4], enhancing[message.author.id][5], enhancing[message.author.id][6]))
					tryagain = False
					expns = enhancing[message.author.id][6] -25
					if expns <= 0:
						expns = 0
					else:
						expns = int(expns/5) +1
					s = "Enhancement __**Successful!**__\nYour 55 Weapon is now: **+{}**\nYou have spent a total of: \n**{:,.2f}** DZ   **{}** <:aethar:435208496510926878> \n**{}** <:normalaetharite:435208601389367297>    **{}** <:weaponupchip:435208556904579093>    **{}** <:antidestruct:435208503880187924>    **{}** <:strengthexpansion:435973634977431553>\n__**{}**__/25 attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], enhancing[message.author.id][2], enhancing[message.author.id][3], enhancing[message.author.id][4], enhancing[message.author.id][5], expns,enhancing[message.author.id][6])
					return s
				else: #fail rate
					if enhancing[message.author.id][0] >= 4:
						enhancing[message.author.id][5] += 1
					enhancing[message.author.id][1] += self.enhancefee[enhancing[message.author.id][0]][0]
					enhancing[message.author.id][2] += self.enhancefee[enhancing[message.author.id][0]][1]
					enhancing[message.author.id][3] += self.enhancefee[enhancing[message.author.id][0]][3]
					enhancing[message.author.id][4] += self.enhancefee[enhancing[message.author.id][0]][2]
					enhancing[message.author.id][6] += 1
					#await m.edit(content="Enhancement __**Failed!**__\nYour 55 Weapon is now: **+{}**\nYou have spent a total of: \n**{:,.2f}** DZ   **{}** <:aethar:435208496510926878> \n**{}** <:normalaetharite:435208601389367297>    **{}** <:weaponupchip:435208556904579093>    **{}** <:antidestruct:435208503880187924>\n__**{}**__/25 attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], enhancing[message.author.id][2], enhancing[message.author.id][3], enhancing[message.author.id][4], enhancing[message.author.id][5], enhancing[message.author.id][6]))
					tryagain = False
					expns = enhancing[message.author.id][6] -25
					if expns <= 0:
						expns = 0
					else:
						expns = int(expns/5) +1
					s = "Enhancement __**Failed!**__\nYour 55 Weapon is now: **+{}**\nYou have spent a total of: \n**{:,.2f}** DZ   **{}** <:aethar:435208496510926878> \n**{}** <:normalaetharite:435208601389367297>    **{}** <:weaponupchip:435208556904579093>    **{}** <:antidestruct:435208503880187924>    **{}** <:strengthexpansion:435973634977431553>\n__**{}**__/25 attempts.".format(enhancing[message.author.id][0], enhancing[message.author.id][1], enhancing[message.author.id][2], enhancing[message.author.id][3], enhancing[message.author.id][4], enhancing[message.author.id][5], expns,enhancing[message.author.id][6])
					return s
			except Exception as e:
				print(e)
				break


	@commands.command(aliases=['urban'])
	@checks.not_lounge()
	async def define(self, ctx, *, word : str = None):
		if word is None:
			await ctx.send('need something to define')
			return
		async with aiohttp.ClientSession() as session:
			async with session.get('http://api.urbandictionary.com/v0/define?term=' + '%20'.join(word.split())) as r:
				tData = await r.json()
				if r.status == 200:
					try:
						i = random.randint(0, len(tData['list'])-1)
						dWord = tData['list'][i]['word']
						dDef = tData['list'][i]['definition']
						dEx = tData['list'][i]['example']
						await ctx.send("__Word__: {}\n__**Definition**__\n{}".format(dWord,dDef,dEx))
					except:
						await ctx.send('Word is not defined')
				else:
					await ctx.send('something went wrong :(')

	@commands.command()
	async def whoisowner(self,ctx):
		await ctx.send("Owner is {}".format(str(ctx.message.guild.owner)))

	@commands.command()
	@checks.not_lounge()
	async def mal(self, ctx, *, anime : str = None):
		message = ctx.message
		if anime is None:
			await ctx.send('https://myanimelist.net/')
			return
		if message.author.id == 94415989378129920:
			await ctx.send('nice try neka <:OMEGALUL:361599663008120833>')
			return
		import xml.etree.ElementTree as ET
		if 'cory in the house' in anime:#this is meme
			embed = discord.Embed()
			embed.title = 'Cory in the House'
			embed.url = 'https://en.wikipedia.org/wiki/Cory_in_the_House'
			embed.color = 1983641
			embed.description="**Name: **{}\n**Status: **{}\n**Air Date: **{}\n**Episodes: **{}\n**Score: **{}\n**Description: **{}".format('コーリー ホワイトハウスでチョー大変! ','Finished','2007-01-12','34','10.00','Cory in the House is an American television series broadcast on the Disney Channel from 2007 to 2008 as a spin-off of the Disney series That’s So Raven, which focused on the exploits of the character Cory Baxter as he and his father take up residence in the White House. The series has since gained an ironic fandom online, including a running joke in which the series is erroneously referred to as an anime. Additionally, members of 4chan’s /v/ (video games) board have attempted to get the Cory in the House Nintendo DS game a most-wanted FAQ page on GameFAQs.')
			embed.set_image(url='http://img.lum.dolimg.com/v1/images/open-uri20150422-12561-zuhjen_2fc6aec3.jpeg?region=0%2C0%2C1000%2C1161')
			embed.set_footer(text='MyAnimeList', icon_url='http://i.imgur.com/8VjfkIQ.png')
			await ctx.send(embed=embed)
			return
		anime = anime.lower().replace(' ', '%20')
		async with aiohttp.ClientSession() as session:
			try:
				async with session.get('https://myanimelist.net/api/anime/search.xml?q=' + anime, auth=aiohttp.BasicAuth(malinfo['User Name'], malinfo['Password'])) as r:
					if r.status == 200:
						ent=0
						if anime.lower().replace('%20', ' ') == 'orange':
							ent = 9
						resp = await r.text()
						tree = ET.fromstring(resp)
						aUrl = 'https://myanimelist.net/anime/' + tree[ent][0].text
						try:
							aName = tree[ent][2].text
							if aName is None:
								aName = tree[ent][1].text
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
						await ctx.send(embed=embed)
					elif r.status == 204:
						await ctx.send("I couldnt find an anime with that name in MyAnimeList")
					else:
						await ctx.send("MyAnimeList is down, NOOOOOOOO :(")
			except:
				await ctx.send("I couldnt find an anime with that name in MyAnimeList")


	@commands.command(hidden=True)
	async def zealisunfair(self, ctx):
		await ctx.send(""":regional_indicator_z: :regional_indicator_e: :regional_indicator_a: :regional_indicator_l:      :regional_indicator_i: :regional_indicator_s:       :regional_indicator_u: :regional_indicator_n: :regional_indicator_f: :regional_indicator_a: :regional_indicator_i: :regional_indicator_r: 

:regional_indicator_c: :regional_indicator_h: :regional_indicator_r: :regional_indicator_i: :regional_indicator_s: :regional_indicator_t: :regional_indicator_i: :regional_indicator_n: :regional_indicator_e:       :regional_indicator_i: :regional_indicator_s:       :regional_indicator_i: :regional_indicator_n:       :regional_indicator_t: :regional_indicator_h: :regional_indicator_e: :regional_indicator_r: :regional_indicator_e:

:regional_indicator_s: :regional_indicator_t: :regional_indicator_a: :regional_indicator_n: :regional_indicator_d: :regional_indicator_i: :regional_indicator_n: :regional_indicator_g:       :regional_indicator_a: :regional_indicator_t:       :regional_indicator_t: :regional_indicator_h: :regional_indicator_e:      :regional_indicator_c: :regional_indicator_o: :regional_indicator_n: :regional_indicator_c: :regional_indicator_e: :regional_indicator_s: :regional_indicator_s: :regional_indicator_i: :regional_indicator_o: :regional_indicator_n:

:regional_indicator_p: :regional_indicator_l: :regional_indicator_o: :regional_indicator_t: :regional_indicator_t: :regional_indicator_i: :regional_indicator_n: :regional_indicator_g:       :regional_indicator_h: :regional_indicator_e: :regional_indicator_r:     :regional_indicator_o: :regional_indicator_p: :regional_indicator_p: :regional_indicator_r: :regional_indicator_e: :regional_indicator_s: :regional_indicator_s: :regional_indicator_i: :regional_indicator_o: :regional_indicator_n:
			""")

	@commands.command(aliases=['twitch'])
	async def checktwitch(self, ctx, twitch : str = None):
		if twitch is None:
			await ctx.send('The format of !checktwitch is `!checktwitch (channelname).`')
			return
		twitch = twitch.lower()
		async with aiohttp.ClientSession() as session:
			async with session.get('https://api.twitch.tv/kraken/streams/{}/?&client_id=4asyzu8i1l7ea1f61aebw3mgbuv04y2'.format(twitch)) as r:
				if r.status == 200:
					tData = await r.json()
					if tData['stream'] == None:
						await ctx.send(twitch+'\'s channel is currently offline!')
					else:
						await ctx.send(twitch+'\'s channel is currently online!\n'+twitch+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+twitch))
				elif r.status == 404:
					await ctx.send('This channel does not exist.')
				elif r.status == 422:
					await ctx.send('Channel ' + twich + ' is a justin.tv channel and doesnt work on twitch or is banned!')

	@commands.command()
	@checks.is_owner()
	async def fancyembed(self, ctx):
		embed = discord.Embed()
		embed.set_author(name="ZeroYami#7235", icon_url="https://cdn.discordapp.com/attachments/222857826165325824/361660545977417729/avatar.jpg")
		embed.title = ">>Dragon Nest Europe Discord link<<"
		embed.url = "https://discord.gg/ymM7jdh"
		embed.description = "The Dragon Nest European Discord"
		embed.color = 0x1E2124
		embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/222857826165325824/361658306630254602/dn-dc-4.png")
		embed.add_field(name="Links",value="[<:dnlogo:362126227676594188>](https://dneu.cherrycredits.com/) [<:facelogo:362125125321097217>](https://www.facebook.com/DragonNestEu/) [<:twit2logo:362127196980248577>](https://twitter.com/dragonnesteu) [<:youtubelogo:362125910570303490>](https://www.youtube.com/user/DragonNestEu)")
		await ctx.send(embed=embed)


	async def regions(self, message):
		for i in MainResponses["regions"]:
			for j in message.author.roles:
				if i in j.name and i.lower() == message.content.lower().replace('!', ''):
					await message.author.remove_roles(discord.utils.get(message.guild.roles, name = i))
					await asyncio.sleep(1)
					return
			if i.lower() == message.content.lower().replace('!', ''):
				await message.author.add_roles(discord.utils.get(message.guild.roles, name = i))
				await asyncio.sleep(1)
				return
	@commands.command(aliases=['Hyperlul','HYPERLUL'])
	async def hyperlul(self,ctx):
		await ctx.send("<:HYPERLUL:266068816528670720>  Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn Ph'nglui mglw'nafh Cthulhu R'lyeh wgah'nagl fhtagn <:HYPERLUL:266068816528670720>")

	@commands.command()
	async def hyejinstar(self,ctx):
		await ctx.send("http://i.imgur.com/SoEdDDZ.png\nhttps://store.na.square-enix.com/product/281427/final-fantasy-xiv-a-realm-reborn-pc-download")

	@commands.command()
	@commands.guild_only()
	async def color(self, ctx):
		message = ctx.message
		if len(message.content.split()) == 1:
			await ctx.send("Type in !colors or !colorlist so I can PM you a list of colors available, then type in `!color (nameofcolor)` for the color you want without the parentheses!")
			return
		rColor = message.content.lower().replace('!color ', '')
		currentcolor = ''
		requestedcolor = ''
		for i in MainResponses["colors"]:
			for j in message.author.roles:
				if i == j.name:
					currentcolor = j.name
			if i.lower().replace("#","").replace(" ","") in rColor.replace("#","").replace(" ",""):
				requestedcolor = i
		if len(requestedcolor) == 0:
			await ctx.send("Couldnt find that color! Make sure to copy the name from the list of colors!")
			return
		elif len(currentcolor) > 0 and len(requestedcolor) > 0:
			oldcolor = discord.utils.get(message.guild.roles, name = currentcolor)
			newcolor = discord.utils.get(message.guild.roles, name = requestedcolor)
			await message.author.remove_roles(oldcolor)
			await asyncio.sleep(1)
			await message.author.add_roles(newcolor)
			await message.author.send("I removed the {} color, and gave you the {} color!".format(currentcolor, requestedcolor))
		elif len(requestedcolor) > 0:
			newcolor = discord.utils.get(message.guild.roles, name = requestedcolor)
			await message.author.add_roles(newcolor)
			await message.author.send("I gave you the {} color!".format(requestedcolor))

	@commands.command(aliases=['colorlist'])
	@commands.guild_only()
	async def colors(self, ctx):
		if ctx.message.guild.id != 106293726271246336:
			return
		await ctx.message.author.send(file=discord.File('C:/DISCORD BOT/Etc/colorlist.png', "colorlist.png"))
		return
	
	async def zealemotes(self, message):
		for i in message.content.lower().split():
			if i.startswith('!') and i.replace('!','').replace(":",";") in bnsEmotes:
				await message.channel.send(file=discord.File('C:/DISCORD BOT/BladeAndSoul/bns_emotes/'+i.replace('!','').replace(":",";")+'.png',i.replace('!','').replace(":",";")+'.png'))
				return

	@commands.command(hidden=True)
	@checks.not_lounge()
	async def deleteian(self, ctx):
		with codecs.open('C:/DISCORD BOT/Etc/daddy.txt','r',"utf-8") as f:
			for i in f:
				await ctx.send(i)
				await asyncio.sleep(2)

	async def bbresponse(self, message):
		if 'who are you' in message.content.lower():
			await message.channel.send('I am a bot that runs on a community made python API(more info on that in bot-and-api channel) and programmed by Comphus to have functions for the Dragon Nest NA Community Discord Server')
			return
		if any(word in message.content.lower() for word in MainResponses['qQuestion']):
			await message.channel.send(MainResponses['magicEight'][random.randint(0,19)]+', ' +  message.author.mention)
			return 
		elif 'hi' in message.content.lower() or 'hello' in message.content.lower():
			await message.channel.send('Hi! ' + message.author.mention)
		elif 'bye' in message.content.lower():
			await message.channel.send('Bye-Bye! ' + message.author.mention)
		elif 'i love you' in message.content.lower() or '<3' in message.content:
			await message.channel.send('I love you too <3 ' + message.author.mention)
		elif 'thank' in message.content.lower():
			await message.channel.send('You\'re welcome! ' + message.author.mention)
		elif 'fuck you' in message.content.lower() or 'fuck u' in message.content.lower() or '( ° ͜ʖ͡°)╭∩╮' in message.content:
			await message.channel.send('( ° ͜ʖ͡°)╭∩╮ ' + message.author.mention)
		else:
			await message.channel.send('what? ' + message.author.mention)

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

	@commands.command(hidden=True)
	async def lightproc(self,ctx):
		await ctx.send('Buckle up!')
		await ctx.send(file=discord.file('C:/DISCORD BOT/Etc/Comphus.jpg', "comphus.jpg"))

	@commands.command(hidden=True)
	@checks.not_lounge()
	async def bruh(self, ctx):
		s = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 😂 👌'
		n = s.split()
		for i in range(15):
			r = random.randint(0, len(n)-1)
			await ctx.message.add_reaction(n[r])

	@commands.command()
	async def whale(self, ctx):
		await ctx.send(file=discord.File("C:/DISCORD BOT/Etc/whale.jpg","whale.png"))

	@commands.command()
	async def saka(self, ctx):
		await ctx.send(""":regional_indicator_h: :regional_indicator_e: :regional_indicator_y:
:regional_indicator_s: :regional_indicator_a: :regional_indicator_k: :regional_indicator_a:
:regional_indicator_y: :regional_indicator_o: :regional_indicator_u:
:regional_indicator_a: :regional_indicator_r: :regional_indicator_e:
:regional_indicator_a: :regional_indicator_n:
:regional_indicator_i: :regional_indicator_d: :regional_indicator_i: :regional_indicator_o: :regional_indicator_t:""")


	@commands.command()
	async def swdmg(self, ctx):
		def intcheck(m):
			return m.content.isdigit() and ctx.message.author == m.author
		await ctx.send("Enter in your attack damage")
		dmg = await self.bot.wait_for("message", check=intcheck, timeout = 30)
		await ctx.send("Enter in your crit%, eg, type 40% crit as 40")
		crit = await self.bot.wait_for("message", check=intcheck, timeout = 30)
		await ctx.send("Enter in your crit damage")
		critdmg = await self.bot.wait_for("message", check=intcheck, timeout = 30)
		await ctx.send("Modifiers? eg: boss damage, type in 15% boss damage as 15")
		modif = await self.bot.wait_for("message", check = lambda m: m.author == ctx.message.author, timeout = 30)
		if modif.content.isdigit():
			modif = (1.00 + int(modif.content)/100.00)
			beforetotal = int(dmg.content) + (int(crit.content)/100.00*int(critdmg.content)) 
			total = int(beforetotal * modif +.5)
			await ctx.send("Formula used: (attack damage + ( crit chance x crit damage)) x modifiers\nInput: ({} + ({}% x {})) = **{}** x {} modifier = **{}**".format(dmg.content,crit.content,critdmg.content,int(beforetotal+.5),modif,total))
		else:
			total = int(int(dmg.content) + (int(crit.content)/100.00*int(critdmg.content)) +.5)
			await ctx.send("Formula used: (attack damage + ( crit chance x crit damage))\nInput: ({} + ({}% x {})) = **{}**".format(dmg.content,crit.content,critdmg.content,total))

	@commands.command(hidden=True)
	async def who(self, ctx):
		if True:
			voice = await ctx.message.author.voice.channel.connect()
			voice.play(discord.FFmpegPCMAudio('C:/DISCORD BOT/Etc/Girl_Cant_Say_Who.wav'))
			await asyncio.sleep(1.7)
			await voice.disconnect()
		#except:
		#	pass

	@commands.command(hidden=True)
	async def piki(self, ctx):
		try:
			voice = await ctx.message.author.voice.channel.connect()
			voice.play(discord.FFmpegPCMAudio('C:/DISCORD BOT/Etc/HEY_HEY_WHATS_SHAKIN.mp3'))
			await asyncio.sleep(2.2)
			await voice.disconnect()
		except:
			pass

	@commands.command(hidden=True)
	async def poi(self, ctx):
		try:
			voice = await ctx.message.author.voice.channel.connect()
			voice.play(discord.FFmpegPCMAudio('C:/DISCORD BOT/Etc/Poi1.mp3'))
			await asyncio.sleep(.8)
			await voice.disconnect()
		except:
			pass

	@commands.command()
	async def kurtzbox(self, ctx, reset : str = None):
		c = ctx.message.author.id
		if c not in boxkurtz:
			boxkurtz[c] = 0
		if reset == "reset":
			boxkurtz[c] = 0
		r = random.randint(0,99)
		s = MainResponses["kurtzbox_sword"]
		if r < 9:
			s = random.choice(s["karma"])
		elif r < 24:
			s = random.choice(s["emote"])
		elif r < 40:
			s = random.choice(s["weapons"])
		elif r < 60:
			s = random.choice(s["dye"])
		else:
			s = random.choice(s["acc"])
		boxkurtz[c] += 1
		await ctx.send("box result: {}\n{} {}\nboxes opened: {}".format(str(ctx.message.author),s[0],s[1],boxkurtz[c]))


	@commands.command(aliases=['commands'])
	async def _commands(self, ctx):
		embed = discord.Embed(description="If you have any questions/requests, feel free to join the BASEDBOT server to ask [here](https://discord.gg/Gvt3Ks8)!")
		embed.set_author(name=str(self.bot.user), icon_url=self.bot.user.avatar_url)
		embed.title = "BASEDBOT Commands"
		embed.url = "https://discord.gg/Gvt3Ks8"
		embed.color = 1983641
		embed.add_field(name="Main Commands", value=MainResponses['all!commands']['!commands'], inline=False)
		embed.add_field(name="Dragon Nest Commands", value=MainResponses['all!commands']['!dncommands'], inline=False)
		embed.add_field(name="Blade And Soul Commands", value=MainResponses['all!commands']['!bnscommands'], inline=False)
		embed.add_field(name="Games", value=MainResponses['all!commands']['!games'], inline=False)
		embed.add_field(name="DNCD/MOD commands", value=MainResponses['all!commands']['!dncdcommands'], inline=False)
		embed.set_footer(text=str(self.bot.user), icon_url=self.bot.user.avatar_url)
		await ctx.message.author.send(embed=embed)

	@commands.command(aliases=list(unicodeResponses.keys()))
	async def unicoderesponses(self, ctx):
		try:
			await ctx.send(unicodeResponses[ctx.message.content.lower().split()[0].strip('!')])
			return
		except:
			await ctx.send("unicode responses are:\n{}".format(list(unicodeResponses.keys())))

	async def mainprefixcommands(self, message):
		if message.content.lower().split()[0] in MainResponses['all!commands'] and message.content.lower().split()[0] not in '!commands':
			if message.content.lower().split()[0] == "!hi":
				print("hi---------------------------------------------------------------------")
			await message.channel.send(MainResponses['all!commands'][message.content.lower().split()[0]])
		if isinstance(message.channel, discord.abc.PrivateChannel) == False and any(reg.lower() in message.content.lower() for reg in MainResponses["regions"]):
			await self.regions(message)

	@commands.Cog.listener()
	async def on_message(self, message):
		if self.bot.user == message.author or message.channel.id == 168949939118800896 or message.author.id == 128044950024617984:
			return
		if message.content.startswith('!'):
			await self.mainprefixcommands(message)
		if '!' in message.content and isinstance(message.channel, discord.abc.PrivateChannel) == False and message.guild.id != 119222314964353025:
			await self.zealemotes(message)
		if message.content.startswith('<@175433427175211008>'):
			await self.bbresponse(message)
		if '/lenny' in message.content.lower():
			await message.channel.send("( ͡° ͜ʖ ͡°)")

def setup(bot):
	bot.add_cog(botetc(bot))
