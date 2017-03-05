import aiohttp
import discord
from bs4 import BeautifulSoup
from discord.ext import commands
from .utils import checks
import io
import json
import random

with open("C:/DISCORD BOT/BladeAndSoul/bnstext.txt") as j:
	bnsurl = j.read()

class bladeandsoul:
	"""
	blade and soul related commands
	in the future if possible, try to reinvent the save build functions to make them more useful
	"""
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True,aliases=["bnsEU","BNSEU","BNSeu"])
	@checks.not_lounge()
	async def bnseu(self, ctx, *, person : str = None):
		await self.bns(ctx, person, "eu")

	@commands.command(pass_context=True,aliases=["bnsNA","BNSNA","BNSna","bns","BNS","Bns"])#default region is NA
	@checks.not_lounge()
	async def bnsna(self, ctx, *, person : str = None):
		await self.bns(ctx, person, "na")

	def bnscolor(self, classname):
		if classname == 'Blade Master':
			return 16718105
		if classname == 'Kung Fu Master':
			return 3325695
		if classname == 'Assassin':
			return 2123412
		if classname == 'Destroyer':
			return 10038562
		if classname == 'Blade Dancer':
			return 7419530
		if classname == 'Soul Fighter':
			return 3066993
		if classname == 'Warlock':
			return 15620599
		if classname == 'Force Master':
			return 15105570
		if classname == 'Summoner':
			return 15844367

	async def bns(self, ctx, person, region):
		link = "http://{}-bns.ncsoft.com/ingame/bs/character/profile?c=".format(region)
		if person is None:
			await self.bot.say('the format for seeing a players bns info is \'!bns (player ign)\'')
			return
		newerM = person.lower()
		if len(newerM.split()) > 1:
			newestM = '%20'.join(newerM.split())
		else:
			newestM = newerM
		if "faggot" in newestM.lower():
			await self.bot.say('http://na-bns.ncsoft.com/ingame/bs/character/profile?c=Rain\nhttp://na-bns.ncsoft.com/ingame/bs/character/profile?c=Minko')
		async with aiohttp.get(link+newestM) as r:
			if r.status == 400:
				await self.bot.say("For some reason the BNS website returned a status code of `400` for {}. Most likely due to Elemental Accessories.".format(person))
				return
			if r.status == 200:
				if "unavailable" in await r.text():
					await self.bot.say("NCSoft says this character information is unavailable\n"+link+'{}&s=101'.format(newestM))
					return

				soup = BeautifulSoup(await r.text(), 'html.parser')
				sig = soup.find_all(attrs={"class":"signature"})
				stat = soup.find_all(attrs={"class":"stat-define"})
				try:
					clan = sig[0].find_all(attrs={"class":"guild"})[0].text
				except:
					clan = 'None'
				classname = sig[0].find_all("ul")[0].li.string
				server = sig[0].find_all("ul")[0].find_all("li")[2].string
				level = sig[0].find_all("li")[1].text.split()[1]
				try:
					hmlevel = sig[0].find_all("li")[1].find_all(attrs={"class":"masteryLv"})[0].string.replace("Level", "**HM:**")
				except:
					hmlevel = "**HM:** 0"
				classicon = soup.find_all("div", class_="classThumb")[0].img['src']
				name = "{}{}".format(soup.find_all("a", href="#")[0].string, soup.find_all("span", attrs={'class':"name"})[0].string)

				#all the main offensive and defensive stats
				att = soup.find_all("div", class_="attack")[0].span.string
				hp = stat[1].find_all(attrs={"class":"stat-title"})[0].find(class_="stat-point").string
				pierce = stat[0].find_all(attrs={"class":"stat-title"})[2].find(class_="stat-point").string
				piercep = stat[0].find_all(attrs={"class":"stat-description"})[2].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
				defense = stat[1].find_all(attrs={"class":"stat-title"})[1].find(class_="stat-point").string
				defensep = stat[1].find_all(attrs={"class":"stat-description"})[1].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
				acc = stat[0].find_all(attrs={"class":"stat-title"})[3].find(class_="stat-point").string
				accp = stat[0].find_all(attrs={"class":"stat-description"})[3].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
				eva = stat[1].find_all(attrs={"class":"stat-title"})[3].find(class_="stat-point").string
				evap = stat[1].find_all(attrs={"class":"stat-description"})[3].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
				chit = stat[0].find_all(attrs={"class":"stat-title"})[5].find(class_="stat-point").string
				chitp = stat[0].find_all(attrs={"class":"stat-description"})[5].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
				block = stat[1].find_all(attrs={"class":"stat-title"})[4].find(class_="stat-point").string
				blockp = stat[1].find_all(attrs={"class":"stat-description"})[4].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[4].string
				cdmg = stat[0].find_all(attrs={"class":"stat-title"})[6].find(class_="stat-point").string
				cdmgp = stat[0].find_all(attrs={"class":"stat-description"})[6].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
				critd = stat[1].find_all(attrs={"class":"stat-title"})[5].find(class_="stat-point").string
				critdp = stat[1].find_all(attrs={"class":"stat-description"})[5].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[1].string

				lft = "**Attack:** {}\n**Pierce:** {}({})\n**Accuracy:** {}({})\n**Critical Hit:** {}({})\n**Critical Damage** {}({})".format(att,pierce,piercep,acc,accp,chit,chitp,cdmg,cdmgp)
				rgt = "**HP:** {}\n**Defense:** {}({})\n**Evasion:** {}({})\n**Block:** {}({})\n**Crit Defense:** {}({})\n".format(hp,defense,defensep,eva,evap,block,blockp,critd,critdp)
				embed = discord.Embed()
				embed.set_author(name=classname, icon_url=classicon)
				embed.title = name
				embed.url = link+newestM
				embed.color = self.bnscolor(classname)
				embed.add_field(name="__General Info__", value="**Server:** {}\n**Clan:** {}\n**Level:** {} \⭐ {}".format(server,clan,level,hmlevel), inline = False)
				embed.add_field(name="__Offensive__", value=lft)
				embed.add_field(name="__Defensive__", value=rgt)
				try:
					weap = soup.find_all("div", class_="wrapWeapon")[0].find_all("p", class_="thumb")[0].img['src']
					embed.set_thumbnail(url=weap)
				except:
					pass
				embed.set_image(url=soup.find_all("div", class_="charaterView")[0].img['src']+"?="+str(random.randint(0,5000)))
				embed.set_footer(text='Blade and Soul', icon_url='http://i.imgur.com/a1kk9Tq.png')
				try:
					await self.bot.say(embed=embed)
				except:#this is a lazy way to check for embeds, since this would also catch other errors
					await self.bot.say("Bot needs embed permissions to display BNS stats")
			else:
				await self.bot.say('Character name does not exist')

	@commands.command(pass_context=True)
	async def bnstree(self, ctx):
		await self.bot.say(self.bnst(ctx.message))

	def bnst(self, message):#this needs to be updated but too lazy
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

	@commands.command(aliases=['bnsm','BNSmarket','BNSm'])
	@checks.not_lounge()
	async def bnsmarket(self, *, item : str = None):
		#await self.bot.say("BNSmarket functions will not work for the time being. This bot used BNSAcademy's live market, and recently NCSoft did something, here is their message ```It seems that due to recent activities of BnSBazaar, NCSOFT has made some changes to how the Marketplace works. Currently, we are unable to keep a working account to push Live Prices. We are actively trying to work on a fix, but sadly, at this time, we have no ETA on when that might be pushed through.```")
		#return
		if item is None:
			await self.bot.say("In order to use the BNS market search function, type in whatever item after you type `!bnsmarket` or `!bnsm` so i can search through <http://www.bns.academy/live-marketplace/> for it.")
			return
		NAparam = {"region": "na", "q": item}
		url = bnsurl
		async with aiohttp.post(url, params=NAparam) as r:
			try:
				NA = await r.json()
			except Exception:
				await self.bot.say("live market website is currently down")
				return
			if r.status != 200:
				await self.bot.say("http://www.bns.academy/live-marketplace/ returned a {} error".format(r.status))
				return
			if "empty" in NA.keys():
				NAparam = {"region": "na", "q": item, "noexact": "true"}
				async with aiohttp.post(url, params=NAparam) as rr:
					NA = await rr.json()
					if "empty" in NA.keys():
						await self.bot.say("Sorry, I couldnt find any item relating to `{}`.".format(item))
		if "noexact" in NAparam.keys():
			EUparam = {"region": "eu", "q": item, "noexact": "true"}
		else:
			EUparam = {"region": "eu", "q": item}
		async with aiohttp.post(url, params=EUparam) as r:
			EU = await r.json()
		NAg, NAs, NAc, EUg, EUs, EUc = 0,0,0,0,0,0#this line doesnt need to be here, but this is just in case the api gets updated with non int numbers
		embed = discord.Embed()
		try:
			iconimg = NA["icon"]#just in case there isnt an icon
			embed.set_thumbnail(url=iconimg)
		except:
			pass
		try:#trying incase bot doesnt have embed permissions
			NAg = NA["gold"]
			NAs = NA["silver"]
			NAc = NA["copper"]
			EUg = EU["gold"]
			EUs = EU["silver"]
			EUc = EU["copper"]
			item = NA["name"]
			embed.set_author(name="Blade & Soul", icon_url="http://i.imgur.com/a1kk9Tq.png")
			embed.title = item
			embed.url = "http://www.bns.academy/live-marketplace/"
			embed.add_field(name="__NA__", value="<:VipGold:248714191517646848>** {} **<:VipSilver:248714227877937152>** {}  **<:VipBronze:248714357792440320>** {}**".format(NAg,NAs,NAc), inline=False)
			embed.add_field(name="__EU__", value="<:VipGold:248714191517646848>** {} **<:VipSilver:248714227877937152>** {}  **<:VipBronze:248714357792440320>** {}**".format(EUg,EUs,EUc))
			embed.color = 3325695
			embed.set_footer(text="Blade & Soul Academy",icon_url="https://cdn.discordapp.com/attachments/275082872203902977/275083108473372673/6.png")
			await self.bot.say(embed=embed)
			return
		except Exception as e:
			if "400" in str(e):
				try:#incase bot doesnt have permission to send messages
					await self.bot.say("This bot needs `Embed` permissions in order to use this function")
					return
				except:
					pass
			pass

	@commands.command()
	async def mspguide(self):
		await self.bot.say('https://drive.google.com/file/d/0Bx5A-bjrg1p1aVlJZElJV3JoWk0/view')

def setup(bot):
	bot.add_cog(bladeandsoul(bot))
