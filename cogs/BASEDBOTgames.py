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

class games:
	def __init__(self, bot):
		self.bot = bot

	def dueling(self, msg):
		duelingInfo = {}#from this line to the end of the 'with open'
		with open('C:/DISCORD BOT/Games/duel.txt') as f:
			a = []
			for i in f:
				a.append(str(i).replace('\n', ''))
			for i in a:
				duelingInfo[i.split()[0].replace('_', ' ')] = [i.split()[1],i.split()[2],i.split()[3]]
		p1 = 0 #p1 and p2 order is set in here
		p2 = 1
		n = msg
		n[0] = '**{}**'.format(n[0].name.replace(' ','_'))
		n[1] = '**{}**'.format(n[1].name.replace(' ','_'))
		people = {}
		people[n[0]] = [10,0] #test fixed status, make it [10,0]
		people[n[1]] = [10,0]
		a = len(duelingInfo)
		if random.randint(0,1) == 0:#checks to see if a random number is either 1 or 0, if its 0, it switches the start order
			p1 = 1
			p2 = 0
		status = ''
		x = 'A coin has been flipped! It decides that ' + n[p1] + ' will go first!'
		z = []
		statCount1 = 0
		statCheck1 = 0
		while people[n[0]][0] > 0 and people[n[1]][0] > 0:
			d = random.randint(0,a-1)
			attack = list(duelingInfo.keys())[d]
			status = int(duelingInfo[attack][2])
			if people[n[p1]][1] == 0:
				crit = 1
				crits = random.randint(0,9)
				revive1 = random.randint(0,9)
				revive2 = random.randint(0,9)
				godAttack = random.randint(0,24)
				actualgodAttack = random.randint(0,99)
				if crits == 0:
					crit = 2
				if godAttack == 0:
					crit *= 10
					z.append("{} transforms into a supreme being, making their next move have a 10x multiplier!".format(n[p1]))
				if actualgodAttack == 0:
					crit *= 100
					z.append("{} became a God, making their next move have a 100x multiplier!".format(n[p1]))
				if attack.count('{}') == 1:
					z.append(attack.format(n[p1]))
					people[n[p1]][0] += (int(duelingInfo[attack][1])*crit)
					people[n[p2]][0] += (int(duelingInfo[attack][0])*crit)
				elif attack.count('{}') == 2:
					z.append(attack.format(n[p1],n[p2]))
					people[n[p1]][0] += (int(duelingInfo[attack][1])*crit)
					people[n[p2]][0] += (int(duelingInfo[attack][0])*crit)
				elif attack.count('{}') == 3:
					z.append(attack.format(n[p1],n[p2],n[p2]))
					people[n[p1]][0] += (int(duelingInfo[attack][1])*crit)
					people[n[p2]][0] += (int(duelingInfo[attack][0])*crit)
				if crits == 0:
					z.append('This attack is a critical hit!')
				z.append('_{} has {} HP left, and {} has {} HP left_'.format(n[0],people[n[0]][0],n[1],people[n[1]][0]))
	
			#applying the status stuns
			rStun = random.randint(0,142)
			if people[n[p1]][1] != 0:
				people[n[p1]][1] -= 1
				if rStun < 14:
					people[n[p1]][1] = 0
					status = 0
					z.append("{} broke free and is able to move! {} becomes immune to CC for 1 turn!".format(n[p1],n[p1]))
			rStun = random.randint(0,142)
			if people[n[p2]][1] != 0:
				people[n[p2]][1] -= 1
				if rStun < 14:
					people[n[p2]][1] = 0
					status = 0
					z.append("{} broke free and is able to move! {} becomes immune to CC for 1 turn!".format(n[p2],n[p2]))
			if status > 0:
				people[n[p2]][1] += abs(status)*crit
			elif status < 0:
				people[n[p1]][1] += abs(status)*crit       
			if people[n[p2]][1] == 0:
				p1, p2 = p2, p1
			if people[n[p1]][0] < 1 and revive1 == 0:
				people[n[p1]][0] = 10
				people[n[p1]][1] = 0
				z.append("**HEROES NEVER DIE!**")
				z.append("{} has been revived with full hp!".format(n[p1]))
			if people[n[p2]][0] < 1 and revive2 == 0:
				people[n[p2]][0] = 10
				people[n[p2]][1] = 0
				z.append("**HEROES NEVER DIE!**")
				z.append("{} has been revived with full hp!".format(n[p2]))


		#checks to see who wins by seeing whoever has 0 or less HP, if both have 0 or less, first if is saved
		endZ = ''            
		if people[n[0]][0] < 1 and people[n[1]][0] < 1:
			endZ += 'They both killed eachother, GG.'
		elif people[n[0]][0] < 1:
			endZ += str(n[1] + ' has beaten ' + n[0] + ' with ' + str(people[n[1]][0]) + ' HP left.')
		elif people[n[1]][0] < 1:
			endZ += str(n[0] + ' has beaten ' + n[1] + ' with ' + str(people[n[0]][0]) + ' HP left.')
			
		"""
		newZ = []
		funC = 1
		contentZ = ('**Battle '+str(funC)+':**\n\n')
		for line in z:
			contentZ += line
			if len(contentZ) > 1850:
				newZ.append(contentZ)
				funC += 1
				contentZ = ('**Battle '+str(funC)+':**\n\n')
		newZ.append(contentZ)
		funC = 0
		"""

		return [z,x,endZ]

	@commands.command(pass_context=True)
	@checks.not_lounge()
	async def duel(self, ctx):
		message = ctx.message
		if len(message.mentions) != 2:
			await self.bot.say('Must have two distinct mentions to duel!')
			return
		results = self.dueling([message.mentions[0],message.mentions[1]])
		await self.bot.say(results[1])
		for i in range(len(results[0])):
			await self.bot.say(results[0][i])
			await asyncio.sleep(3)
		await self.bot.say(results[2])

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
			await self.bot.say("You must mention two people in order to play.")
			return
		players = [message.mentions[0].mention,message.mentions[1].mention]
		results = await self.playrps(players)
		async def rpsresults(r):
			players = [message.mentions[0].mention,message.mentions[1].mention]
			if r[1] == 0:
				await self.bot.say(r[0])
				await self.bot.say("It looks like you two have tied! Would you like to try again {}? Type **yes** or **no**".format(message.author.mention))
				resp = await self.bot.wait_for_message(timeout = 60, author=message.author)
				if resp is None:
					return
				if 'n' in resp.content.lower():
					return
				elif 'y' in resp.content.lower():
					res = await self.playrps(players)
					await rpsresults(res)
					return
			elif r[1] == 1:
				await self.bot.say(r[0])
				return
			elif r[1] == 2:
				await self.bot.upload('C:/Users/gabriel/Pictures/BnS/donkay.png')
				await self.bot.say("You have been visited by the __Mystical__ **DonkaDonks**, you both _Lose_!")
				return
		await rpsresults(results)

	def connect4(self, msg):
		c4 = {}
		thekey = ''
		p1 = []
		p2 = []
		with open("C:/DISCORD BOT/Games/connect4.json") as j:
			c4 = json.load(j)
		if msg.author.id in str(c4.keys()) and msg.content.lower().split()[-1] == 'done':
			for i in c4:
				if msg.author.id in i:
					del c4[i]
					with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
						json.dump(c4, f, indent = 4)
					return 'You have finished your game!'
		if msg.author.id in str(c4.keys()) and msg.content.split()[-1].isdigit() and int(msg.content.split()[-1]) > 0 and int(msg.content.split()[-1]) < 8:
			for i in c4:
				if msg.author.id in i.split()[0]:
					if c4[i]['turn'] == msg.author.id:
						return 'It is not your turn yet.'
					p1 = [i,int(msg.content.split()[-1])-1,msg.author.id]
					thekey = i
					break
				if msg.author.id in i.split()[-1]:
					if c4[i]['turn'] == msg.author.id:
						return 'It is not your turn yet.'
					p2 = [i,int(msg.content.split()[-1])-1,msg.author.id]
					thekey = i
					break
		elif msg.author.id in str(c4.keys()) and (msg.content.split()[-1].isdigit() == False or (int(msg.content.split()[-1]) > 0 and int(msg.content.split()[-1]) < 8) == False):
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
						print('hello2')
						#horizontal check
						if 0 <= y <= 5 and 0 <= x+3 <= 6:
							print('h1')
							if c4[p1[0]][str(y)][x+1] == ":red_circle: " and c4[p1[0]][str(y)][x+2] == ":red_circle: " and c4[p1[0]][str(y)][x+3] == ":red_circle: ":
								print('h2')
								del c4[p1[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going horizontally!\nThe game is now over!'.format(p1[2])
						#vertical check
						if 0 <= y+3 <= 5 and 0 <= x <= 6:
							print('v1')
							if c4[p1[0]][str(y+1)][x] == ":red_circle: " and c4[p1[0]][str(y+2)][x] == ":red_circle: " and c4[p1[0]][str(y+3)][x] == ":red_circle: ":
								print('v2')
								del c4[p1[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going vertically!\nThe game is now over!'.format(p1[2])
						#north east check
						if 0 <= y+3 <= 5 and 0 <= x+3 <= 6:
							print('ne1')
							if c4[p1[0]][str(y+1)][x+1] == ":red_circle: " and c4[p1[0]][str(y+2)][x+2] == ":red_circle: " and c4[p1[0]][str(y+3)][x+3] == ":red_circle: ":
								print('ne2')
								del c4[p1[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going across!\nThe game is now over!'.format(p1[2])
						#south east check
						if 0 <= y-3 <= 5 and 0 <= x+3 <= 6:
							print('se1')
							print(c4[p1[0]][str(y-1)][x+1] == ":red_circle: ")
							print(c4[p1[0]][str(y-2)][x+2] == ":red_circle: ")
							print(c4[p1[0]][str(y-3)][x+3] == ":red_circle: ")
							if c4[p1[0]][str(y-1)][x+1] == ":red_circle: " and c4[p1[0]][str(y-2)][x+2] == ":red_circle: " and c4[p1[0]][str(y-3)][x+3] == ":red_circle: ":
								print('se2')
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
						print('hello1')
						#horizontal check
						if 0 <= y <= 5 and 0 <= x+3 <= 6:
							print('h1')
							if c4[p2[0]][str(y)][x+1] == ":large_blue_circle: " and c4[p2[0]][str(y)][x+2] == ":large_blue_circle: " and c4[p2[0]][str(y)][x+3] == ":large_blue_circle: ":
								print('h2')
								del c4[p2[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going horizontally!\nThe game is now over!'.format(p2[2])
						#vertical check
						if 0 <= y+3 <= 5 and 0 <= x <= 6:
							print('v1')
							if c4[p2[0]][str(y+1)][x] == ":large_blue_circle: " and c4[p2[0]][str(y+2)][x] == ":large_blue_circle: " and c4[p2[0]][str(y+3)][x] == ":large_blue_circle: ":
								print('v2')
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
							print(c4[p2[0]][str(y+1)][x+1] == ":large_blue_circle: ")
							print(c4[p2[0]][str(y+2)][x+2] == ":large_blue_circle: ")
							print(c4[p2[0]][str(y+3)][x+3] == ":large_blue_circle: ")
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
			nm = discord.utils.get(msg.server.members, id = c4[thekey]['turn'])
			if nm.id == thekey.split()[0]:
				c4out += '\n**CURRENT TURN:** {}'.format(discord.utils.get(msg.server.members, id = thekey.split()[-1]).name)
			if nm.id == thekey.split()[-1]:
				c4out += '\n**CURRENT TURN:** {}'.format(discord.utils.get(msg.server.members, id = thekey.split()[0]).name)
			with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
				json.dump(c4, f, indent = 4)
			return c4out

		if len(msg.mentions) != 2:
			return 'You need to mention two people'
		print(str(c4.keys()))
		if msg.author.id not in str(c4.keys()):
			p = '{} vs {}'.format(msg.mentions[0].id, msg.mentions[1].id)
			c4out = '**<@{}> VS <@{}>**\n'.format(p.split()[0],p.split()[-1])
			c4[p] = {}
			for i in range(6):
				c4[p][i] = [':white_circle: ',':white_circle: ',':white_circle: ',':white_circle: ',':white_circle: ',':white_circle: ',':white_circle: ','\n']
			for i in range(6):
				for j in range(8):
					c4out += c4[p][i][j]
			c4out += '-----------------------------------\n   **1**      **2**      **3**     **4**      **5**      **6**      **7**'
			print(c4)
			c4[p]['turn'] = 'None'
			#c4[p]['message'] = [msg.channel.id, msg.id]
			with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
				json.dump(c4, f, indent = 4)

			return c4out

	@commands.command(pass_context=True)
	@checks.not_lounge()
	async def c4(self, ctx):
		message = ctx.message
		c4 = {}
		with open("C:/DISCORD BOT/Games/connect4.json") as j:
			c4 = json.load(j)
		results = self.connect4(message)
		if message.author.id not in str(c4.keys()):
			ms = await self.bot.say(results)
			with open("C:/DISCORD BOT/Games/connect4.json") as j:
				c4 = json.load(j)
			for i in c4:
				if message.author.id in i:
					c4[i]['message'] = [ms.channel.id, ms.id]
			with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
				json.dump(c4, f, indent = 4)
			return
		for i in c4:
			if message.author.id in i:
				if '-----------------------------------\n' in results:
					ch = await self.bot.get_message(self.bot.get_channel(c4[i]['message'][0]), c4[i]['message'][1])
					await self.bot.edit_message(ch, results)
					await self.bot.delete_message(message)
				elif 'won' in results:
					await self.bot.say(results)
					await self.bot.delete_message(message)
				else:
					m = await self.bot.say(results)
					await asyncio.sleep(10)
					await self.bot.delete_message(message)
					await self.bot.delete_message(m)

	@commands.command(pass_context=True)
	async def dntrivia(self, ctx):
		message = ctx.message
		TriviaQuestions = MainResponses['Trivia']
		TriviaQuestion = random.choice(list(TriviaQuestions.keys()))
		await self.bot.say('You have started DN Trivia!\n')
		await asyncio.sleep(1)
		await self.bot.say('You will recieve a question and everyone has 15 seconds to answer it, so be quick! The question is:\n')
		await asyncio.sleep(3)
		await self.bot.say(TriviaQuestion)
		answer = MainResponses['Trivia'][TriviaQuestion]
		end_time = time.time() + 15
		while True:
			time_remaining = end_time - time.time()
			if time_remaining <= 0:
				await self.bot.say('Sorry, you took too long! The answer was '+answer)
				return
			guess = await self.bot.wait_for_message(timeout = time_remaining)
			if guess and answer in guess.content.lower():
				await self.bot.say('Congratulations {}! You\'ve won!'.format(guess.author.mention))
				return

	@commands.command()
	@checks.not_lounge()
	async def battle(self, p1 : discord.Member = None, p2 : discord.Member = None):
		if p1 is None or p2 is None:
			await self.bot.say("need to mention two people")
			return
		results = self.dueling([p1,p2])
		hp = ['10', '10']
		hpform = "__**{}** VS **{}**__\nHP: {}  {}HP: {}".format(str(p1),str(p2), hp[0], ' '*len(str(p1))*2,hp[1])
		t = ['','',results[1]]
		embed = discord.Embed()
		embed.color = 3066993
		embed.description = hpform
		embed.set_thumbnail(url=p2.avatar_url)
		embed.add_field(name='__**BATTLE**__', value="{}\n\n{}\n\n{}".format(t[0],t[1],t[2]), inline=False)
		embed.set_image(url=p1.avatar_url)
		#await self.bot.say(results[1])
		mess = await self.bot.say(embed=embed)
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
				await self.bot.edit_message(mess, embed=embed)
			else:
				hp = [results[0][i].split()[2], results[0][i].split()[8]]
				hpform = "__**{}** VS **{}**__\nHP: {}  {}HP: {}".format(str(p1),str(p2), hp[0], ' '*len(str(p1))*2,hp[1])
				embed = discord.Embed()
				embed.color = 3066993
				embed.description = hpform
				embed.set_thumbnail(url=p2.avatar_url)
				embed.add_field(name='__**BATTLE**__', value="{}\n\n{}\n\n{}".format(t[0],t[1],t[2]), inline=False)
				embed.set_image(url=p1.avatar_url)
				await self.bot.edit_message(mess, embed=embed)
			await asyncio.sleep(3)

		embed = discord.Embed()
		embed.description = hpform
		embed.color = 16718105
		embed.set_thumbnail(url=p2.avatar_url)
		embed.add_field(name='__**BATTLE**__', value="{}\n\n{}\n\n{}".format(t[0],t[1],t[2]), inline=False)
		embed.set_image(url=p1.avatar_url)
		embed.set_footer(text=results[2].replace('*',''))
		await self.bot.edit_message(mess, embed=embed)
		"""
		if member.avatar_url != '':
			embed.set_footer(text=results[2], icon_url=member.avatar_url)
		else:
			embed.set_footer(text=results[2], icon_url=member.default_avatar_url)
		"""

	@commands.command()
	@checks.not_lounge()
	async def superboss(self):
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
		await self.bot.say(embed=embed)
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
				shot = await self.bot.say('{} shoots {}{}'.format(message.author.mention,'(⌐■_■)--︻╦╤─-     ',message.mentions[0].mention))
				for i in shooting:
					await asyncio.sleep(0.1)
					await self.bot.edit_message(shot, '{} shoots {}{}'.format(message.author.mention,i,message.mentions[0].mention))

			elif shootrand < 98:
				shot = await self.bot.say('{}{} the tables have turned! {}'.format(message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',message.mentions[0].mention))
				for i in backshooting:
					await asyncio.sleep(0.1)
					await self.bot.edit_message(shot, '{}{} the theables have turned! {}'.format(message.author.mention,i,message.mentions[0].mention))
			else:
				await self.bot.say('{} and {} make love!'.format(message.author.mention,message.mentions[0].mention))
		elif discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members) != None:
			if shootrand < 89:
				shot = await self.bot.say('{} shoots {}{}'.format(message.author.mention,'(⌐■_■)--︻╦╤─-     ',discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
				for i in shooting:
					await asyncio.sleep(0.1)
					await self.bot.edit_message(shot, '{} shoots {}{}'.format(message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
			elif shootrand < 98:
				shot = await self.bot.say('{}{} the tables have turned! {}'.format(message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
				for i in backshooting:
					await asyncio.sleep(0.1)
					await self.bot.edit_message(shot, '{}{} the tables have turned! {}'.format(message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
			else:
				await self.bot.say('{} and {} make love!'.format(message.author.mention,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()).mention, message.channel.server.members)))


	async def hanging(self, m, sid):
		faces = [
		['<:gachiSANTA:252651283901710336>','/','|','\\','/','\\'],
		['<:dncdDonkay:210492557308723200>','/','|',':ok_hand:','/','\\'],
		[':joy:','/','|',':ok_hand:','/','\\'],
		['<:gachiPRIDE:218901944197054464>','/','|','\\','/','\\']

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

			await self.bot.say("{}\n{}".format(fmt.format(' ',' ',' ',' ',' ',' ',),"".join(wordl)))
			with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
				json.dump(h, f, indent = 4)

			return

		if m is None:
			await self.bot.say("need to enter in your letter guess!")
			return
		else:
			try:
				if len(m) != 1:
					await self.bot.say("you can only guess 1 letter")
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
						await self.bot.say("{}\n{}".format(h[sid][1].replace("{}", " "),"".join(h[sid][2])))
						with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
							json.dump(h, f, indent = 4)
					elif not found:
						h[sid][-1] += 1
						h[sid][1] = h[sid][1].format(h[sid][0][h[sid][-1]-1], *['{}']*(h[sid][1].count('{}')-1))	
						await self.bot.say("{}\n{}".format(h[sid][1].replace("{}", " "),"".join(h[sid][2])))
						with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
							json.dump(h, f, indent = 4)
			except Exception as e:
				print("{}: {}".format(type(e),e))


		with open("C:/DISCORD BOT/Games/hangman.json") as j:
			h = json.load(j)
		if h[sid][1].count('{}') == 0:
			await self.bot.say('You lose!\nThe answer was: **{}**'.format(h[sid][-2]))
			del h[sid]
			with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
				json.dump(h, f, indent = 4)
		elif h[sid][2].count('\\_ ') == 0:
			await self.bot.say("You won!")
			del h[sid]
			with open('C:/DISCORD BOT/Games/hangman.json', 'w') as f:
				json.dump(h, f, indent = 4)

	@commands.command(pass_context=True, aliases=['hang'])
	@checks.not_lounge()
	async def hangman(self, ctx, m:str = None):
		if ctx.message.channel.id != '106293726271246336':
			await self.hanging(m, ctx.message.server.id)

	async def sts(self):
		embed = discord.Embed()
		embed.color = 42080
		embed.set_thumbnail(url='http://www.clipartbest.com/cliparts/yco/4yk/yco4ykLai.jpeg')
		embed.add_field(name='__Stats__', value='LVL: 1\nHP: 10\nMP: 10\nSTR: 4\nINT: 4\nLUK: 4\nWIL: 4\nSTAM: 4')
		embed.set_footer(text='0 remaining skill points',icon_url='http://i.imgur.com/2NzJYy0.png')
		await self.bot.say(embed=embed)

	async def invt(self):
		embed = discord.Embed()
		embed.set_thumbnail(url='http://i.imgur.com/70Bv5Gs.png')
		embed.color = 16032864
		embed.add_field(name='__Inventory__',value='1x - test item 1\n5x - apples\n69x - memes\n42x - dongers\n3x - bananas\n8x - hamburgers\n1x - grey iron sword\n2x - useless candle')
		embed.set_footer(text="1744 Dollars",icon_url='http://ian.umces.edu/imagelibrary/albums/userpics/101505/normal_ian-symbol-dollar-sign.png')
		await self.bot.say(embed=embed)
	async def qst(self):
		embed = discord.Embed()
		embed.set_thumbnail(url='https://cdn.vectorstock.com/i/composite/24,84/quill-ink-pot-icon-vector-32484.jpg')
		embed.color = 13593328
		embed.add_field(name='__Quest Log__',value='1. An adventure worth the risk\n2. Help old man Drake find his memes\n3. Gachi?\n4. The one who struck gold')
		embed.set_footer(text="4 Quests",icon_url='http://pix.iemoji.com/images/emoji/apple/ios-9/256/heavy-exclamation-mark-symbol.png')
		await self.bot.say(embed=embed)
	async def eqp(self):
		embed = discord.Embed()
		embed.set_thumbnail(url='http://www.clker.com/cliparts/4/V/n/C/B/m/sword-and-shield-hi.png')
		embed.color = 42239
		embed.add_field(name='__Equipment__',value='Weapon: Old crooked dagger\nHead: Party sombrero\nArmor: Hardened mud armor\nBoots: Adidas 69s')
		embed.set_footer(text="80 Dollars to repair",icon_url='https://thumbs.dreamstime.com/t/anvil-sledgehammer-cartoon-illustration-53440395.jpg')
		await self.bot.say(embed=embed)
	async def achv(self):
		embed = discord.Embed()
		embed.set_thumbnail(url='http://www.clipartbest.com/cliparts/4c9/kar/4c9karncE.png')
		embed.color = 16777060
		embed.add_field(name='__Achievements__',value='1. Cleaned the toilet!\n2. Golden Finger\n3. Supreme fatty')
		embed.set_footer(text="3 Total Achievements!",icon_url='http://pix.iemoji.com/images/emoji/apple/ios-9/256/glowing-star.png')
		await self.bot.say(embed=embed)

	@commands.command(pass_context=True)
	@checks.not_lounge()
	async def rpg(self, ctx):
		tmt = 30
		await self.bot.say("Would you like to start the BASEDBOT RPG adventure? Type in `yes` or `no`.")
		starting = await self.bot.wait_for_message(author=ctx.message.author,timeout = tmt)
		if starting is None:
			return
		elif 'yes' in starting.content.lower():
			embed = discord.Embed()
			embed.description = "Welcome to the BASEDBOT RPG! This interactive discord RPG experience will require you to actively play, and will timeout and save after 1 minute.\nClick [>>HERE<<](http://i.imgur.com/Ul1WqmV.png) for a quick list of interactive commands you can do with the game!\nType in \"start\" when you are ready for the adventure!"
			embed.color = 13593328
			embed.set_thumbnail(url='https://pbs.twimg.com/media/CQyQbkiUcAEhoQl.jpg')
			await self.bot.say(embed=embed)
			s = await self.bot.wait_for_message(author=ctx.message.author,timeout = tmt)
			if s is None:
				return
			elif 'start' in s.content.lower():
				embed = discord.Embed()
				embed.description = "Welcome! Before we start, lets get used to our commands! Get your ingame commands list out and try some out!"
				embed.set_image(url='http://i.imgur.com/Ul1WqmV.png')
				await self.bot.say(embed=embed)
				async def startgm(acts):
					if acts is None:
						await self.bot.say("session has ended!")
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
						await self.bot.say("Game has been saved and left.")
						return
					g = await self.bot.wait_for_message(author=ctx.message.author,timeout = tmt)
					await startgm(g)

				g = await self.bot.wait_for_message(author=ctx.message.author,timeout = tmt)
				await startgm(g)





def setup(bot):
	bot.add_cog(games(bot))