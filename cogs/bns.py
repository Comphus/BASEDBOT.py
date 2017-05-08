import aiohttp
import discord
from bs4 import BeautifulSoup, Comment
from discord.ext import commands
from .utils import checks
import io
import json
import random

with open("C:/DISCORD BOT/BladeAndSoul/bnstext.txt") as j:
	bnsurl = j.read()
with open("C:/DISCORD BOT/BladeAndSoul/people.json") as j:
	bns_people = json.load(j)

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
			return [16718105, "🔥: {p[fire]}({p[firep]}%)\n⚡: {p[light]}({p[lightp]}%)"]
		if classname == 'Kung Fu Master':
			return [3325695, "🔥: {p[fire]}({p[firep]}%)\n💨: {p[wind]}({p[windp]}%)"]
		if classname == 'Assassin':
			return [2123412, "🌙: {p[shadow]}({p[shadowp]}%)\n⚡: {p[light]}({p[lightp]}%)"]
		if classname == 'Destroyer':
			return [10038562, "🌙: {p[shadow]}({p[shadowp]}%)\n⛰: {p[earth]}({p[earthp]}%)"]
		if classname == 'Blade Dancer':
			return [7419530, "⚡: {p[light]}({p[lightp]}%)\n💨: {p[wind]}({p[windp]}%)"]
		if classname == 'Soul Fighter':
			return [3066993, "❄: {p[frost]}({p[frostp]}%)\n⛰: {p[earth]}({p[earthp]}%)"]
		if classname == 'Warlock':
			return [15620599, "❄: {p[frost]}({p[frostp]}%)\n🌙: {p[shadow]}({p[shadowp]}%)"]
		if classname == 'Force Master':
			return [15105570, "❄: {p[frost]}({p[frostp]}%)\n🔥: {p[fire]}({p[firep]}%)"]
		if classname == 'Summoner':
			return [15844367, "💨: {p[wind]}({p[windp]}%) \n⛰: {p[earth]}({p[earthp]}%)"]

	async def bns(self, ctx, person, region):
		if person is None:
			if ctx.message.author.id in bns_people:
				person = bns_people[ctx.message.author.id]["ign"]
				region = bns_people[ctx.message.author.id]["region"]
			else:
				await self.bot.say('the format for seeing a players bns info is \'!bns (player ign)\'')
				return
		newerM = person.lower()
		if len(newerM.split()) > 1:
			newestM = '%20'.join(newerM.split())
		else:
			newestM = newerM
		if "faggot" in newestM.lower():
			await self.bot.say('http://na-bns.ncsoft.com/ingame/bs/character/profile?c=Rain\nhttp://na-bns.ncsoft.com/ingame/bs/character/profile?c=Minko')
		link = "http://{}-bns.ncsoft.com/ingame/bs/character/data/abilities.json?c={}".format(region,newestM)
		async with aiohttp.get(link) as r:
			#await self.bot.say("currently working on the bns command since NCsoft changed the site")
			if r.status == 400:
				await self.bot.say("For some reason the BNS website returned a status code of `400` for {}. Most likely due to Elemental Accessories.".format(person))
				return
			if r.status == 200:
				#if "unavailable" in await r.text():
				#	await self.bot.say("NCSoft says this character information is unavailable\n"+link+'{}&s=101'.format(newestM))
				#	return

				all_stats = await r.json()
				if all_stats["result"] != "success":
					await self.bot.say("NCSoft says this character information is unavailable\nhttp://{}-bns.ncsoft.com/ingame/bs/character/profile?c={}".format(region, newestM))
					return

				stat = all_stats["records"]["total_ability"]
				HMstat = all_stats["records"]["point_ability"]
				
				sLink = "http://{}-bns.ncsoft.com/ingame/bs/character/profile?c={}".format(region, newestM)
				async with aiohttp.get(sLink) as r:
					soup = BeautifulSoup(await r.text(), 'html.parser')
				sig = soup.find_all(attrs={"class":"signature"})
				try:
					clan = sig[0].find_all(attrs={"class":"guild"})[0].text
				except:
					clan = 'None'
				classname = sig[0].find_all("ul")[0].li.string
				server = sig[0].find_all("ul")[0].find_all("li")[2].string
				level = sig[0].find_all("li")[1].text.split()[1]
				try:
					hmlevel = sig[0].find_all("li")[1].find_all(attrs={"class":"masteryLv"})[0].string.replace("HongmoonLevel", "**HM:**")
				except:
					hmlevel = "**HM:** 0"
				classicon = soup.find_all("div", class_="classThumb")[0].img['src']
				name = "{}{}".format(soup.find_all("a", href="#")[0].string, soup.find_all("span", attrs={'class':"name"})[0].string)

				#HM stat stuff
				hmA = HMstat["offense_point"]
				hmD = HMstat["defense_point"]

				#ATTACK STATS
				att = stat["attack_power_value"]
				pierce = stat["attack_pierce_value"]
				piercep = stat["attack_defend_pierce_rate"]
				acc = stat["attack_hit_value"]
				accp = stat["attack_hit_rate"]
				chit =stat["attack_critical_value"] 
				chitp = stat["attack_critical_rate"]
				cdmg = stat["attack_critical_damage_value"]
				cdmgp = stat["attack_critical_damage_rate"]

				#DEFENSE STATS
				hp = int(stat["max_hp"])
				defense = stat["defend_power_value"]
				defensep = stat["defend_physical_damage_reduce_rate"]
				eva = stat["defend_dodge_value"]
				evap = stat["defend_dodge_rate"]
				block = stat["defend_parry_value"]
				blockp = stat["defend_parry_rate"]
				critd = stat["defend_critical_value"]
				critdp = stat["defend_critical_value"]

				#ELE DAMAGE
				eles = {
					"fire":stat["attack_attribute_fire_value"],
					"firep":stat["attack_attribute_fire_rate"],
					"frost":stat["attack_attribute_ice_value"],
					"frostp":stat["attack_attribute_ice_rate"],
					"wind":stat["attack_attribute_wind_value"],
					"windp":stat["attack_attribute_wind_rate"],
					"earth":stat["attack_attribute_earth_value"],
					"earthp":stat["attack_attribute_earth_rate"],
					"light":stat["attack_attribute_lightning_value"],
					"lightp":stat["attack_attribute_lightning_rate"],
					"shadow":stat["attack_attribute_void_value"],
					"shadowp":stat["attack_attribute_void_rate"]
				}

				#EMBED stuff
				lft = "**Attack:** {} \⭐ {}P\n**Pierce:** {}({}%)\n**Accuracy:** {}({}%)\n**Critical Hit:** {}({}%)\n**Critical Damage** {}({}%)".format(att,hmA,pierce,piercep,acc,accp,chit,chitp,cdmg,cdmgp)
				rgt = "**HP:** {} \⭐ {}P\n**Defense:** {}({}%)\n**Evasion:** {}({}%)\n**Block:** {}({}%)\n**Crit Defense:** {}({}%)\n".format(hp,hmD,defense,defensep,eva,evap,block,blockp,critd,critdp)
				embed = discord.Embed()
				embed.set_author(name=classname, icon_url=classicon)
				embed.title = name
				embed.url = sLink
				cl = self.bnscolor(classname)
				embed.color = cl[0]
				embed.add_field(name="__General Info__", value="**Server:** {}\n**Clan:** {}\n**Level:** {} \⭐ {}".format(server,clan,level,hmlevel))
				#embed.add_field(name='​', value="​")#dummy zero width character field, use this to move the fields around
				embed.add_field(name="__Elemental Damage__", value=cl[1].format(p=eles))
				embed.add_field(name="__Offensive__", value=lft)
				embed.add_field(name="__Defensive__", value=rgt)
				try:
					async with aiohttp.get("http://{}-bns.ncsoft.com/ingame/bs/character/data/equipments.json?c={}".format(region,newestM)) as r:
						gear = await r.json()
					weap = gear["equipments"]["hand"]["equip"]["item"]["icon"]
					embed.set_thumbnail(url=weap)
				except:
					embed.set_thumbnail(url="http://i.imgur.com/yfzrHiy.png")
				if newestM == "rezorector":
					embed.set_image(url="https://cdn.discordapp.com/attachments/204813384888090626/307026647209476101/rezgay.png")
				else:
					embed.set_image(url=soup.find_all("div", class_="charaterView")[0].img['src']+"?="+str(random.randint(0,5000)))
				embed.set_footer(text='Blade and Soul', icon_url='http://i.imgur.com/a1kk9Tq.png')
				try:
					if int(att) >= 1000:
						embed.set_footer(text="Whale and Soul", icon_url="http://i.imgur.com/T6MP5xX.png")
					m = await self.bot.say(embed=embed)
					if int(att) >= 1000:
						try:
							embed.set_footer(text="Whale and Soul", icon_url="http://i.imgur.com/T6MP5xX.png")
							await self.bot.add_reaction(m, "🐋")
						except:
							pass
				except:#this is a lazy way to check for embeds, since this would also catch other errors
					await self.bot.say("Bot needs embed permissions to display BNS stats")
			else:
				await self.bot.say('Character name does not exist')

	@commands.command(pass_context=True, aliases=["bnsl"])
	async def bnslookup(self, ctx, *, member : discord.Member = None):
		if member is None:
			await self.bot.say("Write or mention the name of a person in order to look them up!")
			return
		p = bns_people.get(member.id)
		if p is None:
			await self.bot.say("That person is not in the database")
		else:
			regions = {
				"na":"North America 💵",
				"eu":"Europe 💶"
			}
			newerM = bns_people[member.id]["ign"].lower()
			if len(newerM.split()) > 1:
				newestM = '%20'.join(newerM.split())
			else:
				newestM = newerM
			link = "http://{}-bns.ncsoft.com/ingame/bs/character/profile?c={}".format(bns_people[member.id]["region"],newestM)
			embed = discord.Embed()
			embed.color = 0xFF0000
			embed.set_footer(text="Not Verified! Type !verify to see.",icon_url="http://i.imgur.com/6bdro4H.png")
			embed.url = link
			v = "Not Verified ❌"
			if p.get("verif") == 1:
				v = "Verified ☑"
				embed.color = 0x0066CC
				embed.set_footer(text="Verified!",icon_url="http://i.imgur.com/Ti6nrz3.png")
			embed.set_author(name=str(member),icon_url=member.avatar_url.replace("gif","png"))
			embed.add_field(name="__Character name:__",value=p["ign"])
			embed.add_field(name="__BNS Account Name:__",value=p["acc"])
			embed.add_field(name="__Region:__",value=regions[p["region"].lower()])
			#embed.add_field(name="__Verification Status:__",value=v)
			#embed.description = "__Registered Character name:__ {}\n__BNS Account Name:__ {}\n__Region:__ {}\n__Verification Status:__ {}".format(p["ign"],p["acc"],p["region"],v)
			await self.bot.say(embed=embed)

	@commands.command(pass_context=True,brief="This command tells you how you can get verified")
	async def verify(self, ctx, *,id : str = None):
		if ctx.message.author.id == "90886475373109248" and id is not None:
			try:
				bns_people[id]["verif"] = 1
				with open('C:/DISCORD BOT/BladeAndSoul/people.json', 'w') as f:
					json.dump(bns_people, f, indent = 4)
					await self.bot.say("Account has been verified!☑")
			except:
				await self.bot.say("Verification failed!❌")
			return
		embed = discord.Embed()
		embed.description = "In order to get verified with `!bnslookup`, **you will need to contact Comphus#4981 with proof**. Sending a screenshot of you timestamping ingame with your char name next to it, a timestamp somewhere, and the words \"BASEDBOT\" shown ingame should be fine.\n\n__**Do not**__ friend request Comphus#4981 as he already has too many requests and doesnt know who is who.\n**If you do not have a way to contact him, you may [join the bot server by clicking here to get in contact](https://discord.gg/Gvt3Ks8)**"
		embed.color = 0x0066CC
		await self.bot.say(embed=embed)

	@commands.command(pass_context=True, aliases=["bnss"])
	async def bnssave(self, ctx, region : str = None, *,person : str = None):
		if region is None:
			await self.bot.say("In order to use `!bnssave`, you must provide a region and a main character to save like so `!bnssave region yourchar`, where region is either na or eu.\nOnce saved, you can use `!bns` or `!bnspvp` without having to use your name to pull up the info with the character you saved. In order to remove yourself from the list, type `!bnssave remove`. **This can be used to verify people with `!bnslookup` or aliased `!bnsl` to prevent identity fraud and such.** Type !verify to find out how to get verified\n**If you think someone stole your name, contact Comphus#4981 with !verify**")
			return
		if region.lower() in ("remove","reset"):
			if bns_people.get(ctx.message.author.id) is not None:
				del bns_people[ctx.message.author.id]
				with open('C:/DISCORD BOT/BladeAndSoul/people.json', 'w') as f:
					json.dump(bns_people, f, indent = 4)
					await self.bot.say("You have removed yourself from the list.")
			else:
				await self.bot.say("You are not registered")
			return
		if person is None:
			await self.bot.say("Must provide a character to save/edit")
			return
		if region.lower() == "edit":
			id = ctx.message.author.id
			if bns_people.get(id) is None:
				await self.bot.say("Your are not registered.")
				return
			if True:
				newerM = person.lower()
				if len(newerM.split()) > 1:
					newestM = '%20'.join(newerM.split())
				else:
					newestM = newerM
				link = "http://{}-bns.ncsoft.com/ingame/bs/character/profile?c={}".format(bns_people[id]["region"],newestM)
				print(link)
				async with aiohttp.get(link) as r:
					if r.status != 200:
						await self.bot.say("I could not get the info from the BNS website")
						return
					soup = BeautifulSoup(await r.text(), 'html.parser')
				acc = soup.find_all("a", href="#")[0].string
				name = soup.find_all("span", attrs={'class':"name"})[0].string
				if acc != bns_people[id]["acc"]	:
					await self.bot.say("The account names do not match")
					return
				bns_people[id]["ign"] = name[1:-1]
				with open('C:/DISCORD BOT/BladeAndSoul/people.json', 'w') as f:
					json.dump(bns_people, f, indent = 4)
					await self.bot.say("Character successfully edited")
				return
			try:
				pass
			except:
				await self.bot.say("I could not find the account associated with this character or the website may be down.")
				return

		if region.lower() not in ("na","eu"):
			await self.bot.say("Invalid region, I can only save NA or EU")
			return
		try:
			newerM = person.lower()
			if len(newerM.split()) > 1:
				newestM = '%20'.join(newerM.split())
			else:
				newestM = newerM
			async with aiohttp.get("http://{}-bns.ncsoft.com/ingame/bs/character/profile?c={}".format(region,newestM)) as r:
				soup = BeautifulSoup(await r.text(), 'html.parser')
			id = ctx.message.author.id
			acc = soup.find_all("a", href="#")[0].string
			name = soup.find_all("span", attrs={'class':"name"})[0].string
			if bns_people.get(id) is not None:
				await self.bot.say("Your discord id is already registered.")
				return
			if acc in str(bns_people):
				await self.bot.say("That name is already registered")
				return
			bns_people[id] = {
				"acc":acc,
				"ign":name[1:-1],
				"region":region,
				"verif":0
			}
			with open('C:/DISCORD BOT/BladeAndSoul/people.json', 'w') as f:
				json.dump(bns_people, f, indent = 4)
				await self.bot.say("Character successfully saved")
		except:
			await self.bot.say("I could not find the account associated with this character or the website may be down.")
			return


	@commands.command(pass_context=True, aliases=["bnspvpNA","BNSPVPNA","BNSpvpna","BNSPVPna","bnsp","bnspna","BNSP","Bnsp"])
	async def bnspvp(self, ctx, *, person : str = None):
		await self.pvp(ctx, person, "na")

	@commands.command(pass_context=True, aliases=["bnspvpEU","BNSPVPEU","BNSpvpeu","BNSPVPeu","bnspeu","BNSPEU","Bnspeu"])
	async def bnspvpeu(self, ctx, *, person : str = None):
		await self.pvp(ctx, person, "eu")

	def rRank(self, rank):
		if rank >= 2100:
			return ["http://i.imgur.com/DUxiI7K.png",16770919]
		elif rank >= 1900:
			return ["http://i.imgur.com/DjMO8dP.png",6697881]
		elif rank >= 1600:
			return ["http://i.imgur.com/zGWrxqx.png",16766720]
		elif rank >= 1400:
			return ["http://i.imgur.com/A7UT4yj.png",12632256]
		else:
			return ["http://i.imgur.com/GC4KKXH.png",6700326]
	
	async def pvp(self, ctx, person, region):
		if person is None:
			if ctx.message.author.id in bns_people:
				person = bns_people[ctx.message.author.id]["ign"]
				region = bns_people[ctx.message.author.id]["region"]
			else:
				await self.bot.say('the format for seeing a player\'s pvp info is \'!bnspvp (player ign)\'')
				return
		newerM = person.lower()
		if len(newerM.split()) > 1:
			newestM = '%20'.join(newerM.split())
		else:
			newestM = newerM
		link = "http://{}-bns.ncsoft.com/ingame/bs/character/profile?c={}".format(region, newestM)
		async with aiohttp.get(link) as r:
			if r.status != 200:
				await self.bot.say("Character name does not exist")
				return
			soup = BeautifulSoup(await r.text(), 'html.parser')
		try:
			classicon = soup.find_all("div", class_="classThumb")[0].img['src']
		except:
			pass
		classname = soup.find_all(attrs={"class":"signature"})[0].find_all("ul")[0].li.string
		name = "{}{}".format(soup.find_all("a", href="#")[0].string, soup.find_all("span", attrs={'class':"name"})[0].string)


		testing1 = soup.find_all(class_="characterArea")[0].find_all(text=lambda text:isinstance(text, Comment))[3]
		soup = BeautifulSoup(testing1, 'html.parser')
		p = soup.find_all(class_="season-title")[0].span.string.replace("\n","")
		oneP = int(soup.find_all(class_="rank-point")[0].string)
		if person == "comphus":
			oneP = 2300
		oneW= soup.find_all(class_="win-point")[0].string
		threeP = soup.find_all(class_="rank-point")[1].string
		threeW= soup.find_all(class_="win-point")[1].string
		#await self.bot.say("{}\n1v1 rank:{}    wins:{}\n3v3 rank:{}          wins{}".format(p,oneP,oneW,threeP,threeW))


		embed = discord.Embed()
		embed.set_author(name=classname, icon_url=classicon)
		embed.title = name
		embed.url = link
		ranked = self.rRank(oneP)
		embed.set_thumbnail(url=ranked[0])
		embed.color = ranked[1]
		embed.add_field(name="__Season Games__",value=p.replace("Total "," Total games\n").replace("Wins"," Total Wins"), inline=False)
		embed.add_field(name="1v1 Games",value="Rank:{}\nWins:{}".format(oneP,oneW.replace("Victories ", "")))
		embed.add_field(name="3v3 Games",value="Rank:{}\nWins:{}".format(threeP,threeW.replace("Victories ", "")))

		await self.bot.say(embed=embed)


		#print(soup.find_all(text=lambda text:isinstance(text, Comment)))

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

	@commands.command(aliases=['bnsm','BNSmarket','BNSm',"smp","SMP","Smp"])
	@checks.not_lounge()
	async def bnsmarket(self, *, item : str = None):
		#await self.bot.say("BNSmarket functions will not work for the time being. This bot used BNSAcademy's live market, and recently NCSoft did something, here is their message ```It seems that due to recent activities of BnSBazaar, NCSOFT has made some changes to how the Marketplace works. Currently, we are unable to keep a working account to push Live Prices. We are actively trying to work on a fix, but sadly, at this time, we have no ETA on when that might be pushed through.```")
		#return
		if item is None:
			await self.bot.say("In order to use the BNS market search function, type in whatever item after you type `!bnsmarket`,`!bnsm` or `!smp` so i can search through <http://www.bns.academy/live-marketplace/> for it.")
			return
		NAparam = {"region": "na", "q": item}
		url = bnsurl
		try:
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
		except Exception:
			await self.bot.say("live market website is currently down")
			return
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
			embed.set_footer(text="Blade & Soul Academy",icon_url="http://i.imgur.com/5epeMm5.png	")
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
