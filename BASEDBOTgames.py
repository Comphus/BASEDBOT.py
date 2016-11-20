import asyncio
import discord
from math import *
import time
import random
import json

with open("C:/DISCORD BOT/DiscordStuff/MainResponses.json") as j:
	MainResponses = json.load(j)
with open("C:/DISCORD BOT/Games/triviacontent.json") as j:
	QuizResponses = json.load(j)

class games:
	def __init__(self, bot, message):
		self.bot = bot
		self.message = message

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
		n[0] = '**{}**'.format(n[0].name)
		n[1] = '**{}**'.format(n[1].name)
		people = {}
		people[n[0]] = [10,0] #test fixed status, make it [10,0]
		people[n[1]] = [10,0]
		a = len(duelingInfo)
		if random.randint(0,1) == 0:#checks to see if a random number is either 1 or 0, if its 0, it switches the start order
			p1 = 1
			p2 = 0
		status = ''
		x = 'A coin has been flipped! It decides that ' + n[p1] + ' will go first! \n'
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
				godAttack = random.randint(0,19)
				if crits == 0:
					crit = 2
				if godAttack == 0:
					crit *= 10
					z.append("{}'s transforms into a supreme being, making their next move have a 10x multiplier!\n".format(n[p1]))
				if attack.count('{}') == 1:
					z.append(attack.format(n[p1]) + '\n\n')
					people[n[p1]][0] += (int(duelingInfo[attack][1])*crit)
					people[n[p2]][0] += (int(duelingInfo[attack][0])*crit)
				elif attack.count('{}') == 2:
					z.append(attack.format(n[p1],n[p2]) + '\n\n')
					people[n[p1]][0] += (int(duelingInfo[attack][1])*crit)
					people[n[p2]][0] += (int(duelingInfo[attack][0])*crit)
				elif attack.count('{}') == 3:
					z.append(attack.format(n[p1],n[p2],n[p2]) + '\n\n')
					people[n[p1]][0] += (int(duelingInfo[attack][1])*crit)
					people[n[p2]][0] += (int(duelingInfo[attack][0])*crit)
				if crits == 0:
					z.append('This attack is a critical hit!\n')
				z.append('_{} has {} HP left, and {} has {} HP left_ \n\n'.format(n[0],people[n[0]][0],n[1],people[n[1]][0]))
	
			#applying the status stuns
			rStun = random.randint(0,142)
			if people[n[p1]][1] != 0:
				people[n[p1]][1] -= 1
				if rStun < 14:
					people[n[p1]][1] = 0
					status = 0
					z.append("{} broke free and is able to move! {} becomes immune to CC for 1 turn!\n\n".format(n[p1],n[p1]))
			rStun = random.randint(0,142)
			if people[n[p2]][1] != 0:
				people[n[p2]][1] -= 1
				if rStun < 14:
					people[n[p2]][1] = 0
					status = 0
					z.append("{} broke free and is able to move! {} becomes immune to CC for 1 turn!\n\n".format(n[p2],n[p2]))
			if status > 0:
				people[n[p2]][1] += abs(status)
			elif status < 0:
				people[n[p1]][1] += abs(status)        
			if people[n[p2]][1] == 0:
				p1, p2 = p2, p1
			if people[n[p1]][0] < 1 and revive1 == 0:
				people[n[p1]][0] = 10
				z.append("**HEROES NEVER DIE!**")
				z.append("{} has been revived with full hp!".format(n[p1]))
			if people[n[p2]][0] < 1 and revive2 == 0:
				people[n[p2]][0] = 10
				z.append("**HEROES NEVER DIE!**")
				z.append("{} has been revived with full hp!".format(n[p2]))


		#checks to see who wins by seeing whoever has 0 or less HP, if both have 0 or less, first if is saved
		endZ = ''            
		if people[n[0]][0] < 1 and people[n[1]][0] < 1:
			endZ += '\nThey both killed eachother, GG.'
		elif people[n[0]][0] < 1:
			endZ += str('\n' + n[1] + ' has beaten ' + n[0] + ' with ' + str(people[n[1]][0]) + ' HP left.')
		elif people[n[1]][0] < 1:
			endZ += str('\n' + n[0] + ' has beaten ' + n[1] + ' with ' + str(people[n[0]][0]) + ' HP left.')
			
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

	async def duel(self):
		if len(self.message.mentions) != 2:
			await self.bot.send_message(self.message.channel, 'Must have two distinct mentions to duel!')
			return
		results = self.dueling([self.message.mentions[0],self.message.mentions[1]])
		await self.bot.send_message(self.message.channel, results[1])
		for i in range(len(results[0])):
			await self.bot.send_message(self.message.channel, results[0][i])
			await asyncio.sleep(3)
		await self.bot.send_message(self.message.channel, results[2])

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

	async def rps(self):
		if len(self.message.mentions) != 2:
			await self.bot.send_message(self.message.channel, "You must mention two people in order to play.")
			return
		players = [self.message.mentions[0].mention,self.message.mentions[1].mention]
		results = await self.playrps(players)
		async def rpsresults(r):
			players = [self.message.mentions[0].mention,self.message.mentions[1].mention]
			if r[1] == 0:
				await self.bot.send_message(self.message.channel, r[0])
				await self.bot.send_message(self.message.channel, "It looks like you two have tied! Would you like to try again {}? Type **yes** or **no**".format(self.message.author.mention))
				resp = await self.bot.wait_for_message(timeout = 60, author=self.message.author)
				if resp is None:
					return
				if 'n' in resp.content.lower():
					return
				elif 'y' in resp.content.lower():
					res = await self.playrps(players)
					await rpsresults(res)
					return
			elif r[1] == 1:
				await self.bot.send_message(self.message.channel, r[0])
				return
			elif r[1] == 2:
				await self.bot.send_file(self.message.channel, 'C:/Users/gabriel/Pictures/BnS/donkay.png')
				await self.bot.send_message(self.message.channel, "You have been visited by the __Mystical__ **DonkaDonks**, you both _Lose_!")
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
							print('ne1')
							if c4[p2[0]][str(y-1)][x+1] == ":large_blue_circle: " and c4[p2[0]][str(y-2)][x+2] == ":large_blue_circle: " and c4[p2[0]][str(y-3)][x+3] == ":large_blue_circle: ":
								print('ne2')
								del c4[p2[0]]
								with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
									json.dump(c4, f, indent = 4)
								return 'Congratulations! <@{}> has won with 4 going across!\nThe game is now over!'.format(p2[2])
						#south east check
						if 0 <= y+3 <= 5 and 0 <= x+3 <= 6:
							print('se1')
							print(c4[p2[0]][str(y+1)][x+1] == ":large_blue_circle: ")
							print(c4[p2[0]][str(y+2)][x+2] == ":large_blue_circle: ")
							print(c4[p2[0]][str(y+3)][x+3] == ":large_blue_circle: ")
							if c4[p2[0]][str(y+1)][x+1] == ":large_blue_circle: " and c4[p2[0]][str(y+2)][x+2] == ":large_blue_circle: " and c4[p2[0]][str(y+3)][x+3] == ":large_blue_circle: ":
								print('se2')
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
			nm = discord.utils.get(self.message.server.members, id = c4[thekey]['turn'])
			if nm.id == thekey.split()[0]:
				c4out += '\n**CURRENT TURN:** {}'.format(discord.utils.get(self.message.server.members, id = thekey.split()[-1]).name)
			if nm.id == thekey.split()[-1]:
				c4out += '\n**CURRENT TURN:** {}'.format(discord.utils.get(self.message.server.members, id = thekey.split()[0]).name)
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

	async def c4(self):
		c4 = {}
		with open("C:/DISCORD BOT/Games/connect4.json") as j:
			c4 = json.load(j)
		results = self.connect4(self.message)
		if self.message.author.id not in str(c4.keys()):
			ms = await self.bot.send_message(self.message.channel, results)
			with open("C:/DISCORD BOT/Games/connect4.json") as j:
				c4 = json.load(j)
			for i in c4:
				if self.message.author.id in i:
					c4[i]['message'] = [ms.channel.id, ms.id]
			with open('C:/DISCORD BOT/Games/connect4.json', 'w') as f:
				json.dump(c4, f, indent = 4)
			return
		for i in c4:
			if self.message.author.id in i:
				if '-----------------------------------\n' in results:
					ch = await self.bot.get_message(self.bot.get_channel(c4[i]['message'][0]), c4[i]['message'][1])
					await self.bot.edit_message(ch, results)
					await self.bot.delete_message(self.message)
				elif 'won' in results:
					await self.bot.send_message(self.message.channel, results)
					await self.bot.delete_message(self.message)
				else:
					m = await self.bot.send_message(self.message.channel, results)
					await asyncio.sleep(10)
					await self.bot.delete_message(self.message)
					await self.bot.delete_message(m)

	async def dntrivia(self):
		TriviaQuestions = MainResponses['Trivia']
		TriviaQuestion = random.choice(list(TriviaQuestions.keys()))
		await self.bot.send_message(self.message.channel, 'You have started DN Trivia!\n')
		await asyncio.sleep(1)
		await self.bot.send_message(self.message.channel, 'You will recieve a question and everyone has 15 seconds to answer it, so be quick! The question is:\n')
		await asyncio.sleep(3)
		await self.bot.send_message(self.message.channel, TriviaQuestion)
		answer = MainResponses['Trivia'][TriviaQuestion]
		end_time = time.time() + 15
		while True:
			time_remaining = end_time - time.time()
			if time_remaining <= 0:
				await self.bot.send_message(self.message.channel, 'Sorry, you took too long! The answer was '+answer)
				return
			guess = await self.bot.wait_for_message(timeout = time_remaining)
			if guess and answer in guess.content.lower():
				await self.bot.send_message(self.message.channel, 'Congratulations {}! You\'ve won!'.format(guess.author.mention))
				return

	async def shoots(self):
		shooting = ['(⌐■_■)--︻╦╤─ -    ','(⌐■_■)--︻╦╤─  -   ','(⌐■_■)--︻╦╤─   -  ','(⌐■_■)--︻╦╤─    - ','(⌐■_■)--︻╦╤─     -']
		backshooting = ['    - ─╦╤︻--(■_■ㄱ)','   -  ─╦╤︻--(■_■ㄱ)','  -   ─╦╤︻--(■_■ㄱ)',' -    ─╦╤︻--(■_■ㄱ)','-     ─╦╤︻--(■_■ㄱ)']
		shootrand = random.randint(0,99)

		if len(self.message.mentions) > 0:
			if shootrand < 89:
				shot = await self.bot.send_message(self.message.channel, '{} shoots {}{}'.format(self.message.author.mention,'(⌐■_■)--︻╦╤─-     ',self.message.mentions[0].mention))
				for i in shooting:
					await asyncio.sleep(0.1)
					await self.bot.edit_message(shot, '{} shoots {}{}'.format(self.message.author.mention,i,self.message.mentions[0].mention))

			elif shootrand < 98:
				shot = await self.bot.send_message(self.message.channel, '{}{} the tables have turned! {}'.format(self.message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',self.message.mentions[0].mention))
				for i in backshooting:
					await asyncio.sleep(0.1)
					await self.bot.edit_message(shot, '{}{} the tables have turned! {}'.format(self.message.author.mention,i,self.message.mentions[0].mention))
			else:
				await self.bot.send_message(self.message.channel, '{} and {} make love!'.format(self.message.author.mention,self.message.mentions[0].mention))
		elif discord.utils.find(lambda m: m.name.lower().startswith(self.message.content.split()[1].lower()), self.message.channel.server.members) != None:
			if shootrand < 89:
				shot = await self.bot.send_message(self.message.channel, '{} shoots {}{}'.format(self.message.author.mention,'(⌐■_■)--︻╦╤─-     ',discord.utils.find(lambda m: m.name.lower().startswith(self.message.content.split()[1].lower()), self.message.channel.server.members).mention))
				for i in shooting:
					await asyncio.sleep(0.1)
					await self.bot.edit_message(shot, '{} shoots {}{}'.format(self.message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(self.message.content.split()[1].lower()), self.message.channel.server.members).mention,discord.utils.find(lambda m: m.name.lower().startswith(self.message.content.split()[1].lower()), self.message.channel.server.members).mention))
			elif shootrand < 98:
				shot = await self.bot.send_message(self.message.channel, '{}{} the tables have turned! {}'.format(self.message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',discord.utils.find(lambda m: m.name.lower().startswith(self.message.content.split()[1].lower()), self.message.channel.server.members).mention))
				for i in backshooting:
					await asyncio.sleep(0.1)
					await self.bot.edit_message(shot, '{}{} the tables have turned! {}'.format(self.message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(self.message.content.split()[1].lower()), self.message.channel.server.members).mention))
			else:
				await self.bot.send_message(self.message.channel, '{} and {} make love!'.format(self.message.author.mention,discord.utils.find(lambda m: m.name.lower().startswith(self.message.content.split()[1].lower()).mention, self.message.channel.server.members)))


