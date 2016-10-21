import asyncio
import discord
from math import *
import time
import random
import json

# all types of functions are here
async def rpc(msg):
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

def connect4(msg):
	c4 = {}
	thekey = ''
	p1 = []
	p2 = []
	with open("connect4.json") as j:
		c4 = json.load(j)
	if msg.author.id in str(c4.keys()) and msg.content.lower().split()[-1] == 'done':
		for i in c4:
			if msg.author.id in i:
				del c4[i]
				with open('connect4.json', 'w') as f:
					json.dump(c4, f, indent = 4)
				return 'You have finished your game!'
	if msg.author.id in str(c4.keys()) and type(int(msg.content.split()[-1])) == type(5) and int(msg.content.split()[-1]) > 0 and int(msg.content.split()[-1]) < 8:
		for i in c4:
			if msg.author.id in i.split()[0]:
				p1 = [i,int(msg.content.split()[-1])-1]
				thekey = i
				break
			if msg.author.id in i.split()[-1]:
				p2 = [i,int(msg.content.split()[-1])-1]
				thekey = i
				break
	if len(p1) > 1:
		inc = 0
		prevs = {}
		for i in range(6):
			i = str(i)
			prevs[inc] = i
			if c4[p1[0]][i][p1[1]] == ":white_circle: " and inc < len(c4[p1[0]])-1:
				inc += 1
				continue
			elif c4[p1[0]][i][p1[1]] == ":white_circle: " and inc == len(c4[p1[0]])-1:
				c4[p1[0]][i][p1[1]] = ":red_circle: "
				continue
			elif inc >= 0 and c4[p1[0]][i][p1[1]] != ":white_circle: ":
				try:
					if c4[p1[0]][i][p1[1]] != ":white_circle: ":
						c4[p1[0]][str(int(i)-1)][p1[1]] = ":red_circle: "
						break
				except:
					return 'You cant put your chip there!'
	if len(p2) > 1:
		inc = 0
		prevs = {}
		for i in range(6):
			i = str(i)
			prevs[inc] = i
			if c4[p2[0]][i][p2[1]] == ":white_circle: " and inc < len(c4[p2[0]])-1:
				inc += 1
				continue
			elif c4[p2[0]][i][p2[1]] == ":white_circle: " and inc == len(c4[p2[0]])-1:
				c4[p2[0]][i][p2[1]] = ":large_blue_circle: "
				continue
			elif inc >= 0 and c4[p2[0]][i][p2[1]] != ":white_circle: ":
				try:
					if c4[p2[0]][i][p2[1]] != ":white_circle: ":
						c4[p2[0]][str(int(i)-1)][p2[1]] = ":large_blue_circle: "
						break
				except:
					return 'You cant put your chip there!'
	if len(p1) > 1 or len(p2) > 1:
		c4out = '**<@{}> VS <@{}>**\n'.format(thekey.split()[0],thekey.split()[-1])
		for i in range(6):
			i = str(i)
			for j in range(len(c4[thekey][i])):
				c4out += c4[thekey][i][j]
		c4out += '-----------------------------------\n   **1**      **2**      **3**     **4**      **5**      **6**      **7**'
		with open('connect4.json', 'w') as f:
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
		for i in c4[p]:
			for j in range(len(c4[p][i])):
				c4out += c4[p][i][j]
		c4out += '-----------------------------------\n   **1**      **2**      **3**     **4**      **5**      **6**      **7**'
		print(c4)
		with open('connect4.json', 'w') as f:
			json.dump(c4, f, indent = 4)

		return c4out

def dueling(msg):
	duelingInfo = {}#from this line to the end of the 'with open'
	with open('duel.txt') as f:
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
		#print()
		#print(people[n[p1]][1])
		#print(people[n[p2]][1])
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
