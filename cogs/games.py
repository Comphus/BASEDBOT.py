import asyncio
from discord.ext import commands
import discord
from .utils import checks
from math import *
import time
import random
import json

with open("C:/DISCORD BOT/DiscordStuff/MainResponses.json") as j:
	MainResponses = json.load(j)
with open("C:/DISCORD BOT/Games/triviacontent.json") as j:
	QuizResponses = json.load(j)
potatoes = {}
ded = {}
class games(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.guildQuiz = {}
		self.quizUsers = {}
		self.quizStop = {}
		self.duelCache = {}
		self.royaleCache = {}


	async def potatoed(self, m):
		sid = m.guild.id
		await m.channel.send("Hot potato will start in 10 seconds! all players who were mentioned or left are in the game!\nUse `!hp` to toss the potato, there is a chance that you failed to toss the potato!")
		await asyncio.sleep(10)
		await m.channel.send("Hot potato started! **{}** has the potato!".format(str(ded[sid])))
		counter = 30
		for i in range(30):
			if counter in [25,20,15,10,5,4,3,2,1]:
				await m.channel.send("There are current {} seconds left! **{}** has the potato!".format(counter, str(ded[sid])))
			counter -= 1
			await asyncio.sleep(1)
		lost = ded[sid]
		potatoes[sid].remove(lost)
		await m.channel.send("Times up! It looks like **{}** blew up, eliminating them from the game!".format(str(lost)))
		ded[sid] = random.choice(potatoes[sid])
		if len(potatoes[sid]) == 1:
			await m.channel.send("Congratulations **{}** you survived!".format(potatoes[sid][0]))
			del potatoes[sid]
			del ded[sid]
			return
		await self.potatoed(m)

	@commands.command(pass_context=True, aliases=["hp"])
	async def hotpotato(self, ctx):
		sid = ctx.message.guild.id
		if potatoes.get(sid) is not None and ctx.message.author in potatoes.get(sid):
			ded[sid] = random.choice(potatoes[sid])
			return
		if len(ctx.message.mentions) < 2:
			await ctx.send("you need at least 2 or more people to play")
			return
		if sid not in potatoes:
			potatoes[sid] = ctx.message.mentions
			ded[sid] = random.choice(ctx.message.mentions)
			await self.potatoed(ctx.message)


	def init_players(self,players,hp):
		returnInfo= []
		for i, player in enumerate(players):
			returnInfo.append(#all properties a player has
				{"player":"**{}**".format(player.name),
				"hp":hp,
				"stun":0,
				"immune":0,
				"position":i
				})
		return returnInfo

	#put into asyncio loop
	def dueling(self, entrees, hp):#this is designed to take 2 or more entrees, and returns a simulation of a duel between all participants, specifically only for duels and royale
		with open('C:/DISCORD BOT/Games/duel.json') as f:
			duelingInfo = json.load(f)
		timeouts = time.time() + 10
		players = self.init_players(entrees, hp)
		pLen = len(players)
		p1, p2 = 0, random.randint(1,pLen-1) #p1 is the attacker, p2 is either the other person, or a random other person if more than 2 players
		a = len(duelingInfo)
		duelists = {}
		random.shuffle(players)
		duelists["p1"] = players[0]["player"]#this is the attacker, mainly so json file looks nice
		duelists["p2"] = players[p2]["player"]#this is who ever is the target, it can be one person, or if aoe, everyone else
		x = 'Player ' + players[p1]["player"] + ' has been chosen to go first!'
		z = []
		prettyPlayers = {}
		for i, j in enumerate(players):
			prettyPlayers[j["player"]] = i
		def checkHP(p):
			c = 0
			try:
				for i in p:
					if i["hp"] > 0:
						c += 1
				return c
			except:
				return False
		while checkHP(players) > 1:#makes sure that there are enough players alive to duel
			if time.time() > timeouts:
				print("-------------------------DUEL TIMED OUT DUE TO LONG LOOP----------------.")
				z = ["The duel timed out due to it lasting too long internally."]
				break
			pLen = len(players)
			duelists["p1"] = players[0]["player"]#initialize the attacking player
			for i in range(len(players)):
				prettyPlayers[players[i]["player"]] = i
			p1 = 0
			p2 = random.randint(1,len(players)-1)#assigns next target, in the case of royale, this is a random other person, in duel its just the other person
			duelists["p2"] = players[p2]["player"]
			if players[0]["stun"] == 0 and players[0]["hp"] > 1:#if player is not stunned or dead, goes on
				d = str(random.randint(0,a-1))#gets a random attack
				aoe = False if duelingInfo[d]["aoe"] == "f" else True
				attack, stunned, immune = duelingInfo[d]["name"], int(duelingInfo[d]["stun"]), int(duelingInfo[d]["immune"])
				crit, crits = 1, random.randint(0,9)
				refl = random.randint(0,32)
				swap = random.randint(0,49)
				godAttack, actualgodAttack = random.randint(0,49), random.randint(0,299)
				if crits == 0:
					crit = 2
				if godAttack == 0:
					crit *= 10
					z.append("🌟 {} transforms into a supreme being (2% proc), making their next move have a 10x multiplier! 🌟".format(players[p1]["player"]))
				if actualgodAttack == 0:
					crit *= 100
					z.append("<a:gachiHYPER:393580622439776258> {} became a God (0.33% proc), making their next move have a 100x multiplier! <a:gachiHYPER:393580622439776258>".format(players[p1]["player"]))

				if aoe:#this if else writes down the attack that the player did, if the attack is an aoe, EVERYONE is written instead of just 1 person
					tmp, duelists["p2"] = duelists["p2"], "**EVERYONE**"
					z.append(attack.format(**duelists))
					duelists["p2"] = tmp
				else:
					z.append(attack.format(**duelists))

				if refl == 0:
					z.append("<:mirror:400187507481903104> {} took out Madi's mirror of reversal! All effects damage and effects will be given to the opposite player! <:mirror:400187507481903104>".format(duelists["p2"]))
					p1, p2 = p2, p1 #temporary reversal for mirror
					#duelists["p1"], duelists["p2"] = duelists["p2"], duelists["p1"]
				if swap == 0:#this is a suprise attack made by attacker
					z.append("<:soulexchange:400188292982767617> But then, {} uses Life Exchange! The HP of both players will be swapped! <:soulexchange:400188292982767617>".format(players[0]["player"]))
					players[p1]["hp"], players[p2]["hp"] = players[p2]["hp"], players[p1]["hp"]
				if crits == 0:
					z.append('This attack is a critical hit! <:crit:400189288894955520>')
				#everything before damage is applied
				players[p1]["hp"] += (int(duelingInfo[d]["dmgSelf"])*crit)
				if aoe:
					for i in range(len(players)):
						if i != p1:
							players[i]["hp"] += (int(duelingInfo[d]["dmgEnemy"])*crit)
				else:		
					players[p2]["hp"] += (int(duelingInfo[d]["dmgEnemy"])*crit)
				#effects after damage is applied
				if players[p1]["immune"] > 0 and (int(duelingInfo[d]["dmgSelf"])*crit) < 0:
					z.append("... However, {} is immune to all damage and status effects for the next {} turns!".format(players[p1]["player"], players[p1]["immune"]))
					players[p1]["hp"] -= (int(duelingInfo[d]["dmgSelf"])*crit)
				if aoe:
					for i in range(len(players)):
						if players[i]["immune"] > 0 and (int(duelingInfo[d]["dmgEnemy"])*crit) < 0 and i != p1:
							z.append("... However, {} is immune to all damage and status effects for the next {} turns!".format(players[i]["player"], players[i]["immune"]))
							players[i]["hp"] -= (int(duelingInfo[d]["dmgEnemy"])*crit)
				else:
					if players[p2]["immune"] > 0 and (int(duelingInfo[d]["dmgEnemy"])*crit) < 0:
						z.append("... However, {} is immune to all damage and status effects for the next {} turns!".format(players[p2]["player"], players[p2]["immune"]))
						players[p2]["hp"] -= (int(duelingInfo[d]["dmgEnemy"])*crit)

				endL = []
				for pl in prettyPlayers:
					endL.append("{} has {} HP left".format(pl,players[prettyPlayers[pl]]["hp"]))
				endS = "»» _{}_ ««".format(", ".join(endL))
				z.append(endS)


			#applying the stunned stuns

			for pl in players:
				if pl["stun"] != 0:
					pl["stun"] -= 1
					rStun = random.randint(0,142)
					if rStun < 14:
						pl["stun"] = 0
						z.append("{} broke free and is able to move! {} becomes immune to CC for 1 turn!".format(pl["player"],pl["player"]))
			for pl in players:#this is here to see if it stops the infinite loop
				if pl["immune"] != 0:
					pl["immune"] -= 1
			if stunned < 0 and players[p1]["immune"] == 0:
				players[p1]["stun"] += abs(stunned)*crit
			elif aoe:
				for i in range(len(players)):
					if stunned > 0 and players[i]["immune"] == 0 and i != p1:
						players[i]["stun"] += abs(stunned)*crit
			elif stunned > 0 and players[p2]["immune"] == 0:
				players[p2]["stun"] += abs(stunned)*crit
			stunned = 0
			if immune > 0:
				players[p1]["immune"] += abs(immune)
			elif aoe:
				for i in range(len(players)):
					if immune < 0 and i != p1:
						players[i]["immune"] += abs(immune)
			elif immune < 0:
				players[p2]["immune"] += abs(immune)
			if refl == 0:
				p1, p2 = p2, p1 # undo temporary reversal for mirror
			removePL = []
			for pl in players:
				revive = random.randint(0,9)
				if pl["hp"] < 1 and revive == 0:
					pl["hp"] = hp
					pl["stun"] = 0
					z.append("**HEROES NEVER DIE!**")
					z.append("{} has been revived with full hp!".format(pl["player"]))
				if pl["hp"] < 1:
					z.append("🏳️ {} is unable to fight! 🏳️".format(pl["player"]))
					removePL.append(pl)
			if len(removePL) > 0:
				for pl in removePL:
					players.remove(pl)
					pLen = len(players)
					del prettyPlayers[pl["player"]]
			if len(players) < 2:#if theres only 1 or 0 people left alive, game is finished
				break
			turnCounter = 1
			for i in range(1, len(players)):#this lets the next turn happen, only going if the next person is not stunned
				#try:
				#	print(players)
				#except:
				#	pass
				if players[i]["stun"] == 0:#if whoever is next is not stunned, break out of loop to commence their turn
					break
				elif players[i]["stun"] != 0:#if the person who is next IS stunned, then we add to the counter
					turnCounter += 1
			for i in range(turnCounter):#this loop puts the first person in the list to the back by the value of turnCounter
				players.append(players.pop(0))
			

		#checks to see who wins by seeing whoever has 0 or less HP, if both have 0 or less, first if is saved
		endZ = ''            
		if len(players) == 0:
			endZ += 'They killed eachother, GG.'
		if len(players) == 1:
			endZ += "🎉 {} is the winner with {} HP left! 🎉".format(players[0]["player"],players[0]["hp"])
		return [z,x,endZ]

	@commands.command(pass_context=True)
	@checks.not_lounge()
	async def fight(self, ctx, p1 : discord.Member = None, p2 : discord.Member = None, hp : int = 10):
		message = ctx.message
		results = None
		if hp > 5000:
			await ctx.send('The HP value cannot be greater than 5000')
			return
		if p1 != message.author and p2 is None and p1 is not None:
			p2 = message.author
		if p1 == message.author and p2 is None:
			await ctx.send('Cannot duel yourself!')
			return
		if p1 == p2 or (p1 is None and p2 is None):
			await ctx.send('Must have two distinct mentions, or someone else that isnt you duel!')
			return
		if p1 != p2 and p2 is not None:
			results = await self.bot.loop.run_in_executor(None, lambda: self.dueling([p1,p2], hp))
		await ctx.send("right now im changing fight a bit to look prettier, so expect it to look weird for now. Also, LF> better gifs, looking for a sword swinging/shield pulsing/shield breaking and maybe some more gifs.\n**in order for this new game to work, bot must have embed permissions**")
		embed = discord.Embed()
		embed.color = 0x000000
		embed.set_author(name=results[1],icon_url="http://i.imgur.com/S07dXIT.gif")
		allMessages = []
		m = await ctx.send(embed=embed)
		allMessages.append(m)
		await asyncio.sleep(3)
		embed = discord.Embed()
		embed.color = 0x000000
		embed.set_author(name=results[1],icon_url="http://i.imgur.com/S07dXIT.jpg")
		await m.edit(embed=embed)
		for i in range(len(results[0])):
			embed = discord.Embed()
			embed.color = 3066993
			embed.set_author(name=results[0][i],icon_url="http://i.imgur.com/eFV1CmN.gif")
			#if results[0][i].startswith(("... However,","But then","This attack is a critical hit!")):
			#	m = await m.edit("{} {}".format(m.content, results[0][i]))
			#else:
			m = await ctx.send(embed=embed)
			allMessages.append(m)
			await asyncio.sleep(2.5)
		await ctx.send(results[2])
		for i in allMessages:
			embed = i.embeds[0]
			embed.set_author(name=embed.author.name, icon_url=embed.author.icon_url.replace("gif","png"))
			await i.edit(embed=embed)


	@commands.group(invoke_without_command=True)
	@checks.not_lounge()
	async def royale(self, ctx, *players : discord.Member):
		#print("started royale")
		players = list(set(list(players)))
		message = ctx.message
		results = None
		hp = 10
		if len(players) < 3:
			await ctx.send('need at least 3-10 distinct mentions to start royale')
			return
		if len(players) > 10:
			await ctx.send('Cannot have a royale with more than 10 people')
			return
		#await ctx.send('```Royale may still have some bugs in it, please report them to me in the BASEDBOT discord server which you can find by doing !discord```')
		results = await self.bot.loop.run_in_executor(None, lambda: self.dueling(players, hp))

		m = await ctx.send(results[1])
		for i in players:
			self.duelCache[i.id] = False
		for i in results[0]:
			for k in players:
				if self.duelCache[k.id] is True:
					await ctx.send("Royale has been stopped!")
					for j in players:
						del self.duelCache[j.id]
					return
			if i.startswith(("... However,","But then","This attack is a critical hit!")):
				try:
					await m.edit(content="{} {}".format(m.content, i))
				except Exception as e:
					print(e)
					m = await ctx.send(i)
					print(m)
			else:
				m = await ctx.send(i)
			await asyncio.sleep(3)
		await ctx.send(results[2])


	@royale.command(aliases=['stop'])
	async def royale_stop(self, ctx):
		print("stopped royale")
		stopper = self.duelCache.get(ctx.message.author.id)
		if stopper is not None:
			self.duelCache[ctx.message.author.id] = True

	@commands.group(invoke_without_command=True, description="participants of the duel can use `!duel stop` to stop the duel at any time!")
	@checks.not_lounge()
	async def duel(self, ctx, p1 : discord.Member = None, p2 : discord.Member = None, hp : int = 10):
		#print("started duel")
		#await ctx.send('```Duel may have some bugs due to !royale mode being added in, which is a FFA duel for 3-10 people. If any bugs occur, please report them to me in the BASEDBOT discord server which you can find by doing !discord```')
		if hp > 5000:
			await ctx.send('The HP value cannot be greater than 5000')
			return
		message = ctx.message
		results = None
		if p1 != message.author and p2 is None and p1 is not None:
			p2 = message.author
		if p1 == message.author and p2 is None:
			await ctx.send('Cannot duel yourself!')
			return
		if p1 == p2 or (p1 is None and p2 is None):
			await ctx.send('Must have two distinct mentions, or someone else that isnt you duel!')
			return
		if p1 != p2 and p2 is not None:
			results = await self.bot.loop.run_in_executor(None, lambda: self.dueling([p1,p2], hp))
		#what it spits out
		m = await ctx.send(results[1])
		self.duelCache[p1.id] = False
		self.duelCache[p2.id] = False
		for i in results[0]:
			if self.duelCache[p1.id] is True or self.duelCache[p2.id] is True:
				await ctx.send("Duel has been stopped!")
				del self.duelCache[p1.id]
				del self.duelCache[p2.id]
				return
			if i.startswith(("... However,","But then","This attack is a critical hit!")):
				try:
					await m.edit(content="{} {}".format(m.content, i))
				except Exception as e:
					print(e)
					m = await ctx.send(i)
					print(m)
			else:
				m = await ctx.send(i)
			await asyncio.sleep(3)
		await ctx.send(results[2])

	@duel.command(aliases=['stop'])
	async def duel_stop(self, ctx):
		print("stopped")
		stopper = self.duelCache.get(ctx.message.author.id)
		if stopper is not None:
			self.duelCache[ctx.message.author.id] = True

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if user.guild.id in self.guildQuiz and self.bot.user != user:
			reacts = {
				"\U0001f1e6":"A",
				"\U0001f1e7":"B",
				"\U0001f1e8":"C",
				"\U0001f1e9":"D"
			}
			self.quizUsers[user.guild.id][user] = reacts[reaction.emoji]

	@commands.command(pass_context=True)
	async def quiz(self, ctx):
		message = ctx.message
		if "stop" in message.content.lower():
			self.quizStop[message.guild.id] = True
			return
		if message.guild.id in self.guildQuiz:
			nope = await ctx.send("Quiz already in progress!")
			await asyncio.sleep(3)
			await nope.delete()
			return
		self.guildQuiz[ctx.message.guild.id] = {}
		self.quizUsers[ctx.message.guild.id] = {}
		self.quizStop[message.guild.id] = False
		reacts = ["🇦","🇧","🇨","🇩"]
		with open('C:/DISCORD BOT/Games/quiz.json') as f:
			quizInfo = json.load(f)
		embed = discord.Embed()
		embed.color = 0xffff00
		embed.description = "I'll be giving you multiple questions, in order to answer them you will need to react with the corresponding letter of what you think is the right answer!\nThe game will begin in 15 seconds! Each question will have a 30 second timer!\nuse `!quiz stop` to stop the quiz at any time!"
		await ctx.send("Note: i made this command like a day ago and the system seems to work fine, i just need to add a lot of questions in. these questions will include true/false, and eventually(maybe a week or less from now) i'll add in the ability for everyone to add in quiz questions for their own guilds.",embed=embed)
		await asyncio.sleep(2)
		questLen = len(quizInfo)
		for i in range(questLen):
			if self.quizStop[message.guild.id]:
				await ctx.send("Quiz has been stopped!")
				del self.guildQuiz[message.guild.id]
				del self.quizUsers[message.guild.id]
				del self.quizStop[message.guild.id]
				return
			embed = discord.Embed()
			embed.set_author(name="Dont think too hard.", icon_url="http://i.imgur.com/tEhu1sj.png")
			s = "\n"
			pics = "http://i.imgur.com/nMEnZyd.png"
			question, values = random.choice(list(quizInfo.items()))
			embed.description = "Heres your question!"
			embed.add_field(name="**{}**".format(question), value=s.join(values[0]), inline=False)
			#embed.set_footer(text='30 seconds left', icon_url=pics)
			embed.color = 7419530
			m = await ctx.send(embed=embed)
			for a in reacts:
				await m.add_reaction(a)
			for j in range(29):
				if self.quizStop[message.guild.id]:
					await ctx.send("Quiz has been stopped!")
					del self.guildQuiz[message.guild.id]
					del self.quizUsers[message.guild.id]
					del self.quizStop[message.guild.id]
					return
				counts = [29,28,27,26,20,15,10,5,0]
				if j in counts:
					embed.set_footer(text='{} second(s) left'.format(30-j), icon_url=pics)
					await m.edit(embed=embed)
				await asyncio.sleep(1.05)

			embed.add_field(name="Times up! The answer was:", value=values[1])
			winn = []
			for k in self.quizUsers[message.guild.id]:
				if self.quizUsers[message.guild.id][k].lower() == values[1][0].lower():
					winn.append(str(k))
			if len(winn) == 0:
				winn = ["No one got it right"]
			embed.add_field(name="People who got the answer right:",value = "{}".format(s.join(winn)))
			await m.edit(embed=embed)

			del quizInfo[question]
			await asyncio.sleep(7)

		del self.guildQuiz[message.guild.id]
		del self.quizUsers[message.guild.id]
		del self.quizStop[message.guild.id]




	@commands.command(pass_context=True)
	async def roll(self, ctx, first : int = 100, last : int = None):
		"""
		numreacts = {"0":"0\N{COMBINING ENCLOSING KEYCAP}",
			"1":"1\N{COMBINING ENCLOSING KEYCAP}",
			"2":"2\N{COMBINING ENCLOSING KEYCAP}",
			'3':"3\N{COMBINING ENCLOSING KEYCAP}",
			"4":"4\N{COMBINING ENCLOSING KEYCAP}",
			"5":"5\N{COMBINING ENCLOSING KEYCAP}",
			"6":"6\N{COMBINING ENCLOSING KEYCAP}",
			"7":"7\N{COMBINING ENCLOSING KEYCAP}",
			"8":"8\N{COMBINING ENCLOSING KEYCAP}",
			"9":"9\N{COMBINING ENCLOSING KEYCAP}"}
		"""
		if last is None:
			r = random.randint(0,first)
			await ctx.send("{} You rolled a **{}**!(0-{})".format(ctx.message.author.mention, r,first))
		elif last is not None:
			r = random.randint(first,last)
			await ctx.send("{} You rolled a **{}**!({}-{})".format(ctx.message.author.mention, r,first,last))
	
	async def playrps(self, msg):
		att = {0:':fist:',1:':hand_splayed:',2:':v:'}
		a = random.randint(0,2)
		b = random.randint(0,2)
		egg = random.randint(0,99)
		players = {a:msg[0],b:msg[1]}
		r = '{} -> {}        {} <- {}'.format(msg[0],att[a],att[b],msg[1])
		if egg > 94:
			return ['',2]
		if b > a:
			high = b
			low = a
		elif b < a:
			high = a
			low = b
		if a == b:
			return [r,0]
		elif a != b:
			if a+b == 1:
				win = '\n**{} has won!**'.format(players[high])
				w = r+win
				return [w,1]
			elif a+b == 2:
				win = '\n**{} has won!**'.format(players[low])
				w = r+win
				return [w,1]
			elif a+b == 3:
				win = '\n**{} has won!**'.format(players[high])
				w = r+win
				return [w,1]

	@commands.command(pass_context=True)
	@checks.not_lounge()
	async def rps(self, ctx):
		message = ctx.message
		if len(message.mentions) != 2:
			await ctx.send("You must mention two people in order to play.")
			return
		players = [message.mentions[0].mention,message.mentions[1].mention]
		results = await self.playrps(players)
		async def rpsresults(r):
			players = [message.mentions[0].mention,message.mentions[1].mention]
			if r[1] == 0:
				await ctx.send(r[0])
				await ctx.send("It looks like you two have tied! Would you like to try again {}? Type **yes** or **no**".format(message.author.mention))
				def pred(m):
					return m.author == message.author
				try:
					resp = await self.bot.wait_for("message", timeout = 60, check=pred)
				except asyncio.TimeoutError:
					return
				else:
					if 'n' in resp.content.lower():
						return
					elif 'y' in resp.content.lower():
						res = await self.playrps(players)
						await rpsresults(res)
						return
			elif r[1] == 1:
				await ctx.send(r[0])
				return
			elif r[1] == 2:
				await ctx.send(file=discord.File('C:/Users/gabriel/Pictures/donkay.png',"donkay.png"))
				await ctx.send("You have been visited by the __Mystical__ **DonkaDonks**, you both _Lose_!")
				return
		await rpsresults(results)

	def connect4(self, msg): # this can be changed A LOT to have a lot less code
		mid = str(msg.author.id)
		c4 = {}
		thekey = ''
		p1 = []
		p2 = []
		with open("C:/DISCORD BOT/Games/connect4.json") as j:
			c4 = json.load(j)
		if mid in str(c4.keys()) and msg.content.lower().split()[-1] == 'done':
			for i in c4:
				if mid in i:
					del c4[i]
					with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
						json.dump(c4, f, indent = 4)
					return 'You have finished your game!'
		if mid in str(c4.keys()) and msg.content.split()[-1].isdigit() and int(msg.content.split()[-1]) > 0 and int(msg.content.split()[-1]) < 8:
			for i in c4:
				if mid in i.split()[0]:
					if c4[i]['turn'] == mid:
						return 'It is not your turn yet.'
					p1 = [i,int(msg.content.split()[-1])-1,mid]
					thekey = i
					break
				if mid in i.split()[-1]:
					if c4[i]['turn'] == mid:
						return 'It is not your turn yet.'
					p2 = [i,int(msg.content.split()[-1])-1,mid]
					thekey = i
					break
		elif mid in str(c4.keys()) and (msg.content.split()[-1].isdigit() == False or (int(msg.content.split()[-1]) > 0 and int(msg.content.split()[-1]) < 8) == False):
			return 'You need to input a number from 1-7'
		if len(p1) > 1:
			c4[p1[0]]['turn'] = p1[2]
			inc = 0
			prevs = {}
			for i in range(6):
				i = str(i)
				prevs[inc] = i
				if c4[p1[0]][i][p1[1]] == ":white_circle: " and inc < 5:
					inc += 1
					continue
				elif c4[p1[0]][i][p1[1]] == ":white_circle: " and inc == 5:
					c4[p1[0]][i][p1[1]] = ":red_circle: "
					continue
				elif inc >= 0 and c4[p1[0]][i][p1[1]] != ":white_circle: ":
					try:
						if c4[p1[0]][i][p1[1]] != ":white_circle: ":
							c4[p1[0]][str(int(i)-1)][p1[1]] = ":red_circle: "
							break
					except:
						return 'You cant put your chip there!'
			#winner check after p1 move
			for y in range(6):
				for x in range(7):
					if c4[p1[0]][str(y)][x] == ":red_circle: ":
						#horizontal check
						if 0 <= y <= 5 and 0 <= x+3 <= 6:
							if c4[p1[0]][str(y)][x+1] == ":red_circle: " and c4[p1[0]][str(y)][x+2] == ":red_circle: " and c4[p1[0]][str(y)][x+3] == ":red_circle: ":
								del c4[p1[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going horizontally!\nThe game is now over!'.format(p1[2])
						#vertical check
						if 0 <= y+3 <= 5 and 0 <= x <= 6:
							if c4[p1[0]][str(y+1)][x] == ":red_circle: " and c4[p1[0]][str(y+2)][x] == ":red_circle: " and c4[p1[0]][str(y+3)][x] == ":red_circle: ":
								del c4[p1[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going vertically!\nThe game is now over!'.format(p1[2])
						#north east check
						if 0 <= y+3 <= 5 and 0 <= x+3 <= 6:
							if c4[p1[0]][str(y+1)][x+1] == ":red_circle: " and c4[p1[0]][str(y+2)][x+2] == ":red_circle: " and c4[p1[0]][str(y+3)][x+3] == ":red_circle: ":
								del c4[p1[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going across!\nThe game is now over!'.format(p1[2])
						#south east check
						if 0 <= y-3 <= 5 and 0 <= x+3 <= 6:
							if c4[p1[0]][str(y-1)][x+1] == ":red_circle: " and c4[p1[0]][str(y-2)][x+2] == ":red_circle: " and c4[p1[0]][str(y-3)][x+3] == ":red_circle: ":
								del c4[p1[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going across!\nThe game is now over!'.format(p1[2])

		if len(p2) > 1:
			c4[p2[0]]['turn'] = p2[2]
			inc = 0
			prevs = {}
			for i in range(6):
				i = str(i)
				prevs[inc] = i
				if c4[p2[0]][i][p2[1]] == ":white_circle: " and inc < 5:
					inc += 1
					continue
				elif c4[p2[0]][i][p2[1]] == ":white_circle: " and inc == 5:
					c4[p2[0]][i][p2[1]] = ":large_blue_circle: "
					continue
				elif inc >= 0 and c4[p2[0]][i][p2[1]] != ":white_circle: ":
					try:
						if c4[p2[0]][i][p2[1]] != ":white_circle: ":
							c4[p2[0]][str(int(i)-1)][p2[1]] = ":large_blue_circle: "
							break
					except:
						return 'You cant put your chip there!'
			#winner check after p2 move
			for y in range(6):
				for x in range(7):
					if c4[p2[0]][str(y)][x] == ":large_blue_circle: ":
						#horizontal check
						if 0 <= y <= 5 and 0 <= x+3 <= 6:
							if c4[p2[0]][str(y)][x+1] == ":large_blue_circle: " and c4[p2[0]][str(y)][x+2] == ":large_blue_circle: " and c4[p2[0]][str(y)][x+3] == ":large_blue_circle: ":
								del c4[p2[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going horizontally!\nThe game is now over!'.format(p2[2])
						#vertical check
						if 0 <= y+3 <= 5 and 0 <= x <= 6:
							if c4[p2[0]][str(y+1)][x] == ":large_blue_circle: " and c4[p2[0]][str(y+2)][x] == ":large_blue_circle: " and c4[p2[0]][str(y+3)][x] == ":large_blue_circle: ":
								del c4[p2[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going vertically!\nThe game is now over!'.format(p2[2])
						#north east check
						if 0 <= y-3 <= 5 and 0>= x+3 <= 6:
							#print('ne1')
							if c4[p2[0]][str(y-1)][x+1] == ":large_blue_circle: " and c4[p2[0]][str(y-2)][x+2] == ":large_blue_circle: " and c4[p2[0]][str(y-3)][x+3] == ":large_blue_circle: ":
								#print('ne2')
								del c4[p2[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going across!\nThe game is now over!'.format(p2[2])
						#south east check
						if 0 <= y+3 <= 5 and 0 <= x+3 <= 6:
							#print('se1')
							if c4[p2[0]][str(y+1)][x+1] == ":large_blue_circle: " and c4[p2[0]][str(y+2)][x+2] == ":large_blue_circle: " and c4[p2[0]][str(y+3)][x+3] == ":large_blue_circle: ":
								#print('se2')
								del c4[p2[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going across!\nThe game is now over!'.format(p2[2])

		if len(p1) > 1 or len(p2) > 1:
			c4out = '**<@{}> VS <@{}>**\n'.format(thekey.split()[0],thekey.split()[-1])
			for i in range(6):
				i = str(i)
				for j in range(8):
					c4out += c4[thekey][i][j]
			c4out += '-----------------------------------\n   **1**      **2**      **3**     **4**      **5**      **6**      **7**'
			nm = self.bot.get_user(int(c4[thekey]['turn']))
			if str(nm.id) == thekey.split()[0]:
				c4out += '\n**CURRENT TURN:** {}'.format(self.bot.get_user(int(thekey.split()[-1])).name)
			if str(nm.id) == thekey.split()[-1]:
				c4out += '\n**CURRENT TURN:** {}'.format(self.bot.get_user(int(thekey.split()[0])).name)
			with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
				json.dump(c4, f, indent = 4)
			return c4out

		if len(msg.mentions) != 2:
			return 'You need to mention two people'
		if mid not in str(c4.keys()):
			p = '{} vs {}'.format(msg.mentions[0].id, msg.mentions[1].id)
			c4out = '**<@{}> VS <@{}>**\n'.format(p.split()[0],p.split()[-1])
			c4[p] = {}
			for i in range(6):
				c4[p][i] = [':white_circle: ',':white_circle: ',':white_circle: ',':white_circle: ',':white_circle: ',':white_circle: ',':white_circle: ','\n']
			for i in range(6):
				for j in range(8):
					c4out += c4[p][i][j]
			c4out += '-----------------------------------\n   **1**      **2**      **3**     **4**      **5**      **6**      **7**'
			c4[p]['turn'] = 'None'
			#c4[p]['message'] = [msg.channel.id, msg.id]
			with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
				json.dump(c4, f, indent = 4)

			return c4out

	@commands.command(pass_context=True)
	@checks.not_lounge()
	async def c4(self, ctx):
		message = ctx.message
		mid = str(message.author.id)
		c4 = {}
		with open("C:/DISCORD BOT/Games/connect4.json") as j:
			c4 = json.load(j)
		results = self.connect4(message)
		if mid not in str(c4.keys()):
			ms = await ctx.send(results)
			with open("C:/DISCORD BOT/Games/connect4.json") as j:
				c4 = json.load(j)
			for i in c4:
				if mid in i:
					c4[i]['message'] = [ms.channel.id, ms.id]
			with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
				json.dump(c4, f, indent = 4)
			return
		for i in c4:
			if mid in i:
				if '-----------------------------------\n' in results:
					ch = await ctx.get_message(int(c4[i]['message'][1]))
					await ch.edit(content=results)
					await message.delete()
				elif 'won' in results:
					await ctx.send(results)
					await message.delete()
				else:
					m = await ctx.send(results)
					await asyncio.sleep(10)
					await message.delete()
					await m.delete()

	@commands.command(pass_context=True)
	async def dntrivia(self, ctx):
		message = ctx.message
		TriviaQuestions = MainResponses['Trivia']
		TriviaQuestion = random.choice(list(TriviaQuestions.keys()))
		await ctx.send('You have started DN Trivia!\n')
		await asyncio.sleep(1)
		await ctx.send('You will recieve a question and everyone has 15 seconds to answer it, so be quick! The question is:\n')
		await asyncio.sleep(3)
		await ctx.send(TriviaQuestion)
		answer = MainResponses['Trivia'][TriviaQuestion]
		end_time = time.time() + 15
		while True:
			time_remaining = end_time - time.time()
			if time_remaining <= 0:
				await ctx.send('Sorry, you took too long! The answer was '+answer)
				return
			guess = await self.bot.wait_for("message",timeout = time_remaining)
			if guess and answer in guess.content.lower():
				await ctx.send('Congratulations {}! You\'ve won!'.format(guess.author.mention))
				return

	@commands.command()
	@checks.not_lounge()
	async def battle(self, ctx, p1 : discord.Member = None, p2 : discord.Member = None):
		if p1 is None or p2 is None:
			await ctx.send("need to mention two people")
			return
		results = await self.bot.loop.run_in_executor(None, lambda: self.dueling([p1,p2], 10))
		hp = ['10', '10']
		hpform = "__**{}** VS **{}**__\nHP: {}  {}HP: {}".format(str(p1),str(p2), hp[0], ' '*len(str(p1))*2,hp[1])
		t = ['','',results[1]]
		embed = discord.Embed()
		embed.color = 3066993
		embed.description = hpform
		embed.set_thumbnail(url=p2.avatar_url)
		embed.add_field(name='__**BATTLE**__', value="{}\n\n{}\n\n{}".format(t[0],t[1],t[2]), inline=False)
		embed.set_image(url=p1.avatar_url)
		#await ctx.send(results[1])
		mess = await ctx.send(embed=embed)
		await asyncio.sleep(3)
		for i in range(len(results[0])):
			if 'HP left_' not in results[0][i]:
				t.pop(0)
				t.append(results[0][i])
				embed = discord.Embed()
				embed.color = 3066993
				embed.description = hpform
				embed.set_thumbnail(url=p2.avatar_url)
				embed.add_field(name='__**BATTLE**__', value="{}\n\n{}\n\n{}".format(t[0],t[1],t[2]), inline=False)
				embed.set_image(url=p1.avatar_url)
				await mess.edit(embed=embed)
			else:
				hp = [results[0][i].split()[2], results[0][i].split()[8]]
				hpform = "__**{}** VS **{}**__\nHP: {}  {}HP: {}".format(str(p1),str(p2), hp[0], ' '*len(str(p1))*2,hp[1])
				embed = discord.Embed()
				embed.color = 3066993
				embed.description = hpform
				embed.set_thumbnail(url=p2.avatar_url)
				embed.add_field(name='__**BATTLE**__', value="{}\n\n{}\n\n{}".format(t[0],t[1],t[2]), inline=False)
				embed.set_image(url=p1.avatar_url)
				await mess.edit(embed=embed)
			await asyncio.sleep(3)

		embed = discord.Embed()
		embed.description = hpform
		embed.color = 16718105
		embed.set_thumbnail(url=p2.avatar_url)
		embed.add_field(name='__**BATTLE**__', value="{}\n\n{}\n\n{}".format(t[0],t[1],t[2]), inline=False)
		embed.set_image(url=p1.avatar_url)
		embed.set_footer(text=results[2].replace('*',''))
		await mess.edit(embed=embed)
		"""
		if member.avatar_url != '':
			embed.set_footer(text=results[2], icon_url=member.avatar_url)
		else:
			embed.set_footer(text=results[2], icon_url=member.default_avatar_url)
		"""

	
	@commands.command(pass_context=True, aliases=["lb"])
	@checks.not_lounge()
	async def lootbox(self, ctx):
		colors = {
			"common":0xFFFFFF,
			"rare":0x65C6F6,
			"epic":0xE46DF6,
			"legend":0xFDEC54
		}
		lb = "http://i.imgur.com/b6LUfbd.png"
		t = "Recieved {} {} {}!"
		heroes = ['Genji', 'McCree', 'Pharah', 'Reaper', 'Soldier 76', 'Sombra', 'Tracer', 'Bastion', 'Hanzo', 'Junkrat', 'Mei', 'Torbjörn', 'Widowmaker', 'D.Va', 'Orisa', 'Reinhardt', 'Roadhog', 'Winston', 'Zarya', 'Ana', 'Lúcio', 'Mercy', 'Symmetra', 'Zenyatta']
		items = ["Spray","Skin","voice line","emote","victory pose","highlight intro"]
		rareCheck = 0
		embed = discord.Embed()
		for i in range(4):
			r1 = random.randint(0,43)#epic chance
			r2 = random.randint(0,107)#legendary chance
			r3 = random.choice(heroes)
			r4 = random.choice(items)
			if r1 in (0,1):
				embed.set_author(name=t.format("an Epic",r3,r4),icon_url=lb)
				embed.color = colors["epic"]
			elif r2 in (0,1):
				embed.set_author(name=t.format("a Legendary",r3,r4),icon_url=lb)
				embed.color = colors["legend"]
			else:
				r = random.choice(["Rare","Common"])
				if r == "Common":
					rareCheck += 1
				if rareCheck == 3:
					r = "Rare"
				embed.set_author(name=t.format("a "+r,r3,r4),icon_url=lb)
				embed.color = colors[r.lower()]
			await ctx.send(embed=embed)
			await asyncio.sleep(0.4)





	@commands.command(pass_context=True)
	@checks.not_lounge()
	async def slots(self, ctx, roll : int = 3):
		theemojis = """
		<:gachiGASM:266068765979049984> <:HYPERLUL:266068816528670720> :cherries: :pear: :apple: :taco: :strawberry: :cookie:   :seven: :six_pointed_star: :star2: :star: :grapes: :lemon: :peach: :gorilla: :star_of_david: :100: 
		"""
		newemojis = theemojis.split()
		results = []
		for i in range(roll):
			r = random.randint(0,len(newemojis)-1)
			results.append(newemojis[r])
		b = 1
		for i in results:
			if results.count(i) > 1:
				if results.count(i) > b:
					b = results.count(i)
		if b == 1:
			await ctx.send("**{}** rolled these slots!\n{}\n\nand lost!(1/{})".format(ctx.message.author.name,str(results).replace(",", " ").replace("'", ""),len(results)))
		elif b < len(results):
			await ctx.send("**{}** rolled these slots!\n{}\n\nand almost won!({}/{})".format(ctx.message.author.name,str(results).replace(",", " ").replace("'", ""),b,len(results)))
		elif b == len(results):
			await ctx.send("**{}** rolled these slots!\n{}\n\nand IS A WINNER!!!({}/{})".format(ctx.message.author.name,str(results).replace(",", " ").replace("'", ""),len(results),len(results)))
	@commands.command()
	@checks.not_lounge()
	async def superboss(self,ctx):
		bosses = {
		0:["KILLER KITCHEN CLEANING TOOL","❤❤❤❤❤❤❤","http://vignette3.wikia.nocookie.net/spongebob/images/8/89/Drifter.png/revision/latest?cb=20150728004136",0],
		1:["EXPAND DONG","❤❤❤❤❤❤❤❤❤❤\n❤❤❤❤❤❤❤❤❤❤\n❤❤❤❤❤❤❤❤❤❤","http://vignette1.wikia.nocookie.net/donkeykong/images/5/52/FunkyTF.png/revision/latest?cb=20140308130438",9830655],
		2:["NUMBAH ONE 「ナンバーワン」","❤❤❤❤❤❤❤❤❤❤\n❤❤❤❤❤❤❤❤❤❤\n❤❤❤❤❤❤❤❤❤❤\n💛💛💛💛💛💛💛💛💛💛\n💛💛💛💛💛💛💛💛💛💛","http://vignette2.wikia.nocookie.net/straight-bunch/images/1/11/Robbie_Rotten_lazytown_02.gif/revision/latest?cb=20130512013614",16766720],
		3:["MY SWAMP", "❤❤❤❤","http://honilands.co.uk/img/blog_entries/7ebd7_Shrek_fierce.jpg",0],
		4:["B.O.R.K","❤❤❤❤❤❤❤❤❤❤\n❤❤❤❤❤","https://i.ytimg.com/vi/xUPGVxKUNao/maxresdefault.jpg",34303]
		}
		r = random.randint(0,4)
		embed = discord.Embed()
		embed.description = "**{}**\n{}".format(bosses[r][0],bosses[r][1])
		embed.color = bosses[r][3]
		embed.set_image(url=bosses[r][2])
		await ctx.send(embed=embed)
		#embed.set_thumbnail(url="http://vignette1.wikia.nocookie.net/donkeykong/images/5/52/FunkyTF.png/revision/latest?cb=20140308130438")
		#embed.add_field(name='​', value="​", inline=False)
		#embed.add_field(name='​', value="​", inline=False)
		#embed.add_field(name='​', value="-----------------\n| What will      |\n| You do           |\n-----------------",)
		#embed.add_field(name='​', value="​")
		#embed.add_field(name='​', value="​---------------------------\n|     FIGHT       |    BAG    |\n|POKEMON   |    RUN    |\n---------------------------")
		#embed.set_footer(text='❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤❤')

	@commands.command(pass_context=True)
	async def shoot(self, ctx):
		message = ctx.message
		shooting = ['(⌐■_■)--︻╦╤─ -    ','(⌐■_■)--︻╦╤─  -   ','(⌐■_■)--︻╦╤─   -  ','(⌐■_■)--︻╦╤─    - ','(⌐■_■)--︻╦╤─     -']
		backshooting = ['    - ─╦╤︻--(■_■ㄱ)','   -  ─╦╤︻--(■_■ㄱ)','  -   ─╦╤︻--(■_■ㄱ)',' -    ─╦╤︻--(■_■ㄱ)','-     ─╦╤︻--(■_■ㄱ)']
		shootrand = random.randint(0,99)

		if len(message.mentions) > 0:
			if shootrand < 89:
				shot = await ctx.send('{} shoots {}{}'.format(message.author.mention,'(⌐■_■)--︻╦╤─-     ',message.mentions[0].mention))
				for i in shooting:
					await asyncio.sleep(0.1)
					await shot.edit(content='{} shoots {}{}'.format(message.author.mention,i,message.mentions[0].mention))

			elif shootrand < 98:
				shot = await ctx.send('{}{} the tables have turned! {}'.format(message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',message.mentions[0].mention))
				for i in backshooting:
					await asyncio.sleep(0.1)
					await shot.edit(content='{}{} the the tables have turned! {}'.format(message.author.mention,i,message.mentions[0].mention))
			else:
				await ctx.send('{} and {} make love!'.format(message.author.mention,message.mentions[0].mention))
		elif discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.guild.members) != None:
			if shootrand < 89:
				shot = await ctx.send('{} shoots {}{}'.format(message.author.mention,'(⌐■_■)--︻╦╤─-     ',discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.guild.members).mention))
				for i in shooting:
					await asyncio.sleep(0.1)
					await shot.edit(content='{} shoots {}{}'.format(message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.guild.members).mention,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.guild.members).mention))
			elif shootrand < 98:
				shot = await ctx.send('{}{} the tables have turned! {}'.format(message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.guild.members).mention))
				for i in backshooting:
					await asyncio.sleep(0.1)
					await shot.edit(content='{}{} the tables have turned! {}'.format(message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.guild.members).mention))
			else:
				await ctx.send('{} and {} make love!'.format(message.author.mention,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()).mention, message.channel.guild.members)))


	async def hanging(self, ctx, m, sid):
		faces = [
		['<:gachiGASM:266068765979049984>','/','|','\\',':mans_shoe: ',':mans_shoe: '],
		['<:dncdDonkay:210492557308723200>','/','|',':ok_hand:',':mans_shoe: ',':mans_shoe: '],
		[':joy:','/','|',':ok_hand:',':mans_shoe: ',':mans_shoe: '],
		['<:gachiPRIDE:218901944197054464>','/','|','\\',':mans_shoe: ',':mans_shoe: ']

		]
		fmt = """\_\_\_\_\_\_
|          |
|      {} 
|        {}{}{}
|        {} {}
|
|
"""
		word = ""
		wordl = ["\_ "]
		with open("C:/DISCORD BOT/Games/hangman.json") as j:
			h = json.load(j)
		if sid not in h.keys():
			face = faces[random.randint(0, len(faces)-1)]
			word = h['words'][random.randint(0, len(h['words'])-1)]
			wordl = wordl * len(word)
			h[sid] = [face,fmt,wordl,word,0]

			await ctx.send("{}\n{}".format(fmt.format(' ',' ',' ',' ',' ',' ',),"".join(wordl)))
			with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
				json.dump(h, f, indent = 4)

			return

		if m is None:
			await ctx.send("need to enter in your letter guess!")
			return
		else:
			try:
				if len(m) != 1:
					await ctx.send("you can only guess 1 letter")
					return
				else:
					found = False
					ind = {}
					ind[m.lower()] = []
					for i in range(len(h[sid][3])):
						if m.lower() == h[sid][3][i].lower():	
							ind[m.lower()].append(i)
							found = True
					if found:
						for i in range(len(ind[m.lower()])):
							h[sid][2][ind[m.lower()][i]] = '__{}__ '.format(m.lower())
						await ctx.send("{}\n{}".format(h[sid][1].replace("{}", " "),"".join(h[sid][2])))
						with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
							json.dump(h, f, indent = 4)
					elif not found:
						h[sid][-1] += 1
						h[sid][1] = h[sid][1].format(h[sid][0][h[sid][-1]-1], *['{}']*(h[sid][1].count('{}')-1))	
						await ctx.send("{}\n{}".format(h[sid][1].replace("{}", " "),"".join(h[sid][2])))
						with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
							json.dump(h, f, indent = 4)
			except Exception as e:
				print("{}: {}".format(type(e),e))

		with open("C:/DISCORD BOT/Games/hangman.json") as j:
			h = json.load(j)
		if h[sid][1].count('{}') == 0:
			await ctx.send('You lose!\nThe answer was: **{}**'.format(h[sid][-2]))
			del h[sid]
			with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
				json.dump(h, f, indent = 4)
		elif h[sid][2].count('\\_ ') == 0:
			await ctx.send("You won!")
			del h[sid]
			with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
				json.dump(h, f, indent = 4)

	@commands.command()
	async def myd(self, ctx):
		r = random.randint(1,5050)
		d = r/100
		await ctx.send("your d is... **{} inches!**".format(d))

	@commands.command()
	async def myv(self, ctx):
		r = random.randint(1,5050)
		d = r/100
		await ctx.send("your v is... **{} inches!**".format(d))

	@commands.command(pass_context=True, aliases=['hang'])
	@checks.not_lounge()
	async def hangman(self, ctx, m:str = None):
		if ctx.message.channel.id != '106293726271246336':
			await self.hanging(ctx, m, ctx.message.guild.id)

	async def sts(self, ctx):
		embed = discord.Embed()
		embed.color = 42080
		embed.set_thumbnail(url='http://www.clipartbest.com/cliparts/yco/4yk/yco4ykLai.jpeg')
		embed.add_field(name='__Stats__', value='LVL: 1\nHP: 10\nMP: 10\nSTR: 4\nINT: 4\nLUK: 4\nWIL: 4\nSTAM: 4')
		embed.set_footer(text='0 remaining skill points',icon_url='http://i.imgur.com/2NzJYy0.png')
		await ctx.send(embed=embed)
	async def invt(self, ctx):
		embed = discord.Embed()
		embed.set_thumbnail(url='http://i.imgur.com/70Bv5Gs.png')
		embed.color = 16032864
		embed.add_field(name='__Inventory__',value='1x - test item 1\n5x - apples\n69x - memes\n42x - dongers\n3x - bananas\n8x - hamburgers\n1x - grey iron sword\n2x - useless candle')
		embed.set_footer(text="1744 Dollars",icon_url='http://ian.umces.edu/imagelibrary/albums/userpics/101505/normal_ian-symbol-dollar-sign.png')
		await ctx.send(embed=embed)
	async def qst(self):
		embed = discord.Embed()
		embed.set_thumbnail(url='https://cdn.vectorstock.com/i/composite/24,84/quill-ink-pot-icon-vector-32484.jpg')
		embed.color = 13593328
		embed.add_field(name='__Quest Log__',value='1. An adventure worth the risk\n2. Help old man Drake find his memes\n3. Gachi?\n4. The one who struck gold')
		embed.set_footer(text="4 Quests",icon_url='http://pix.iemoji.com/images/emoji/apple/ios-9/256/heavy-exclamation-mark-symbol.png')
		await ctx.send(embed=embed)
	async def eqp(self):
		embed = discord.Embed()
		embed.set_thumbnail(url='http://www.clker.com/cliparts/4/V/n/C/B/m/sword-and-shield-hi.png')
		embed.color = 42239
		embed.add_field(name='__Equipment__',value='Weapon: Old crooked dagger\nHead: Party sombrero\nArmor: Hardened mud armor\nBoots: Adidas 69s')
		embed.set_footer(text="80 Dollars to repair",icon_url='https://thumbs.dreamstime.com/t/anvil-sledgehammer-cartoon-illustration-53440395.jpg')
		await ctx.send(embed=embed)
	async def achv(self):
		embed = discord.Embed()
		embed.set_thumbnail(url='http://www.clipartbest.com/cliparts/4c9/kar/4c9karncE.png')
		embed.color = 16777060
		embed.add_field(name='__Achievements__',value='1. Cleaned the toilet!\n2. Golden Finger\n3. Supreme fatty')
		embed.set_footer(text="3 Total Achievements!",icon_url='http://pix.iemoji.com/images/emoji/apple/ios-9/256/glowing-star.png')
		await ctx.send(embed=embed)

	@commands.command(hidden=True)
	@checks.not_lounge()
	async def rpg(self, ctx):
		tmt = 30
		await ctx.send("Would you like to start the BASEDBOT RPG adventure? Type in `yes` or `no`.")
		def pred(m):
			return m.author == message.author
		starting = await self.bot.wait_for("message", check=pred,timeout = tmt)
		if starting is None:
			return
		elif 'yes' in starting.content.lower():
			embed = discord.Embed()
			embed.description = "Welcome to the BASEDBOT RPG! This interactive discord RPG experience will require you to actively play, and will timeout and save after 1 minute.\nClick [>>HERE<<](http://i.imgur.com/Ul1WqmV.png) for a quick list of interactive commands you can do with the game!\nType in \"start\" when you are ready for the adventure!"
			embed.color = 13593328
			embed.set_thumbnail(url='https://pbs.twimg.com/media/CQyQbkiUcAEhoQl.jpg')
			await ctx.send(embed=embed)
			s = await self.bot.wait_for("message", check=pred,timeout = tmt)
			if s is None:
				return
			elif 'start' in s.content.lower():
				embed = discord.Embed()
				embed.description = "Welcome! Before we start, lets get used to our commands! Get your ingame commands list out and try some out!"
				embed.set_image(url='http://i.imgur.com/Ul1WqmV.png')
				await ctx.send(embed=embed)
				async def startgm(acts):
					if acts is None:
						await ctx.send("session has ended!")
						return
					elif 'inv' in acts.content.lower():
						await self.invt()
					elif 'stat' in acts.content.lower():
						await self.sts()
					elif 'quest' in acts.content.lower():
						await self.qst()
					elif 'equip' in acts.content.lower() or 'gear' in acts.content.lower():
						await self.eqp()
					elif 'achieve' in acts.content.lower():
						await self.achv()
					elif 'leave game' in acts.content.lower():
						await ctx.send("Game has been saved and left.")
						return
					g = await self.bot.wait_for("message", check=pred,timeout = tmt)
					await startgm(g)

				g = await self.bot.wait_for("message", check=pred,timeout = tmt)
				await startgm(g)


def setup(bot):
	bot.add_cog(games(bot))