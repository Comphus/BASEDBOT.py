import discord
import asyncio
from datetime import datetime
import requests
import json
import fileinput
import io
from math import *
import time
import random
import logging
import codecs
import shelve
if not discord.opus.is_loaded():
	discord.opus.load_opus('opus')
logging.basicConfig()
client = discord.Client()


twitchEmotes = []
MainResponses = {}
dLogin={}
voice = None
player = None
musicQue = []
timeoutStore = 0
powerTimeout = {}
with open('twitch.txt') as inputF:
	twitchEmotes = inputF.read().splitlines()
with open("MainResponses.json") as j:
	MainResponses = json.load(j)
with open("C:/discordlogin.json") as j:
	dLogin = json.load(j)
dMods = []
dAdmins = []
with open('Mods.txt','r') as f:
	for i in f:
		dMods.append(str(i).replace('\n', ''))

with open('Admins.txt','r') as f:
	for i in f:
		dAdmins.append(str(i).replace('\n', ''))






unicodeResponses = {'/lenny':'( ͡° ͜ʖ ͡°)','!gardenintool':'(  ′︵‵  )/','/shrug':'¯\ _(ツ)_/¯'}




# all types of functions are here
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
			if attack.count('{}') == 1:
				z.append(attack.format(n[p1]) + '\n\n')
				people[n[p1]][0] += int(duelingInfo[attack][1])
				people[n[p2]][0] += int(duelingInfo[attack][0])
			elif attack.count('{}') == 2:
				z.append(attack.format(n[p1],n[p2]) + '\n\n')
				people[n[p1]][0] += int(duelingInfo[attack][1])
				people[n[p2]][0] += int(duelingInfo[attack][0])
			elif attack.count('{}') == 3:
				z.append(attack.format(n[p1],n[p2],n[p2]) + '\n\n')
				people[n[p1]][0] += int(duelingInfo[attack][1])
				people[n[p2]][0] += int(duelingInfo[attack][0])
		
		#applying the status stuns
		if people[n[p1]][1] != 0:
			people[n[p1]][1] -= 1
		if people[n[p2]][1] != 0:
			people[n[p2]][1] -= 1
		if status > 0:
			people[n[p2]][1] += abs(status)
		elif status < 0:
			people[n[p1]][1] += abs(status)        
		if people[n[p2]][1] == 0:
			p1, p2 = p2, p1


	#checks to see who wins by seeing whoever has 0 or less HP, if both have 0 or less, first if is saved
	endZ = ''            
	if people[n[0]][0] < 1 and people[n[1]][0] < 1:
		endZ += '\nThey both killed eachother, GG.'
	elif people[n[0]][0] < 1:
		endZ += str('\n' + n[1] + ' has beaten ' + n[0] + ' with ' + str(people[n[1]][0]) + ' HP left.')
	elif people[n[1]][0] < 1:
		endZ += str('\n' + n[0] + ' has beaten ' + n[1] + ' with ' + str(people[n[0]][0]) + ' HP left.')
		
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

	return [newZ,x,endZ]




@client.async_event
def on_member_join(member):
	if member.server.id != '110373943822540800':
		yield from client.send_message(member.server.channels[0], 'Welcome ' + member.mention + ' to the server!')
		print(member)
		t = datetime.now()
		if str(member.server.id) == '106293726271246336':
			with io.open('joinLog.txt','a',encoding='utf-8') as f:
				retS = ('Name: ' +str(member.name)+ ' ID:' + str(member.id)+ ' Time joined:' + str(t) + ' EST\n')
				f.write(retS)


@client.async_event
def on_message(message):

	global timeoutStore
	global powerTimeout
	global voice
	global player
	global musicQue
	cTime = datetime.now()

	if timeoutStore > 0:
		for i in powerTimeout:
			timeDiff = cTime - powerTimeout[i][1]
			if timeDiff.seconds >= powerTimeout[i][0]:
				client.remove_roles(powerTimeout[i][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
				powerTimeout.pop(i)
				timeoutStore -= 1
				break
	if message.content.startswith('!timeout') and str(message.author.id) in dAdmins and len(message.content.split()) == 3 and type(int(message.content.split()[2])) == type(1):
		newM = message.content.split()
		t1 = datetime.now()
		powerTimeout[newM[1]] = [int(newM[2]),t1,message.mentions[0]]
		timeoutStore += 1
		yield from client.add_roles(message.mentions[0], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
		yield from client.send_message(message.channel, newM[1]+' has been timed out for '+newM[2]+' seconds.')
	elif message.content.startswith('!timeout') and str(message.author.id) in dAdmins:
		yield from client.send_message(message.channel, 'The format for timing someone out is !timeout @ mention (timeinseconds)')
	if message.content.startswith('!stoptimeout') and str(message.author.id) in dAdmins and len(message.content.split()) == 2:
		newM = message.content.split()
		if newM[1] in powerTimeout:
			yield from client.remove_roles(powerTimeout[newM[1]][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
			powerTimeout.pop(newM[1])
			yield from client.send_message(message.channel, newM[1]+'\'s timeout has been manually stopped.')
		elif 'Jail' in discord.utils.find(lambda m: m.name == 'Jail', message.channel.server.members).roles:
			yield from client.remove_roles(powerTimeout[newM[1]][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
			yield from client.send_message(message.channel, newM[1]+'\'s timeout has been manually stopped.')
		else:
			yield from client.send_message(message.channel, 'That person has not been manually timed out.')
	elif message.content.startswith('!stoptimeout') and str(message.author.id) in dAdmins:
		yield from client.send_message(message.channel, 'The format for timing someone out is !timeout @ mention')

	if message.content.startswith('!') == False:
		for t in twitchEmotes:
			if t in message.content:
				yield from client.send_file(message.channel, 'C:/DISCORD BOT/twitch emotes/'+t+'.jpg')
				break
	elif message.content.lower().split()[0] in MainResponses['all!commands']:
		yield from client.send_message(message.channel, MainResponses['all!commands'][message.content.lower().split()[0]])

	if message.content.startswith('!test'):
		logs = yield from client.logs_from(message.channel, limit=100)
		counter = 0
		tmp = yield from client.send_message(message.channel, 'Calculating messages...')
		for log in logs:
			if log.author == message.author:
				counter += 1
		yield from client.edit_message(tmp, 'You have {} messages.'.format(counter))
	elif message.content in unicodeResponses:
		yield from client.send_message(message.channel, unicodeResponses[message.content.lower().split()[0]])
	elif message.content.startswith('!sleep'):
		yield from asyncio.sleep(5)
		yield from client.send_message(message.channel, 'Done sleeping')
	elif message.content.startswith('!hello'):
		yield from client.send_message(message.channel, 'hi')
	elif message.content.startswith('!duel') and str(message.channel.id) not in '91518345953689600':	
		results = dueling([message.mentions[0].mention,message.mentions[1].mention])
		yield from client.send_message(message.channel, results[1])
		for i in range(len(results[0])):
			yield from client.send_message(message.channel, results[0][i])
			yield from client.send_message(message.channel, results[2])
	elif message.content.startswith('!trivia'):
		TriviaQuestions = MainResponses['Trivia']
		TriviaQuestion = random.choice(list(TriviaQuestions.keys()))
		yield from client.send_message(message.channel, 'You have started DN Trivia!\n')
		yield from asyncio.sleep(1)
		yield from client.send_message(message.channel, 'You will recieve a question and everyone has 15 seconds to answer it, so be quick! The question is:\n')
		yield from asyncio.sleep(3)
		yield from client.send_message(message.channel, TriviaQuestion)
		answer = MainResponses['Trivia'][TriviaQuestion]
		end_time = time.time() + 15
		while True:
			time_remaining = end_time - time.time()
			if time_remaining <= 0:
				yield from client.send_message(message.channel, 'Sorry, you took too long! The answer was '+answer)
				return
			guess = yield from client.wait_for_message(timeout = time_remaining)
			print(guess)
			if guess and answer in guess.content.lower():
				yield from client.send_message(message.channel, 'Congratulations {}! You\'ve won!'.format(guess.author.mention))
				return
	if True: #message.channel.server.id == '106293726271246336':
		if message.content.startswith("!yt") and len(message.content.split()) == 2:
			if voice == None:
				voice = yield from client.join_voice_channel(message.author.voice_channel)
				#voice = yield from client.join_voice_channel(discord.utils.get(client.get_all_channels(), id ='129079702403940352')) to make it only go to voice channel for bot in dn discord
			if 'stop' in message.content:
				if voice.is_connected():
					yield from voice.disconnect()
					musicQue = []
					return

			endurl = message.content.split()[1]
			if 'https://www.youtube.com/watch?v=' in endurl:
				endurl = endurl.replace('https://www.youtube.com/watch?v=', '')
			musicQue.append(endurl)
			if 'next' in message.content and player != None and len(musicQue) >0:
				if voice.is_connected():
					player.stop()
					#musicQue.pop()
			def playmusicque(voice, queurl):
				global player
				try:
					if queurl == "next":
						musicQue.pop(0)
						pass
					elif player != None:
						player.stop()
						player = voice.create_ytdl_player('https://www.youtube.com/watch?v='+queurl)
						player.start()
						musicQue.pop(0)
					else:
						player = voice.create_ytdl_player('https://www.youtube.com/watch?v='+queurl)
						player.start()
						musicQue.pop(0)
				except Exception as e:
					musicQue.pop(0)
					yield from client.send_message(message.channel, e)
			if player == None:
				if len(musicQue) == 1:
					yield from playmusicque(voice, musicQue[0])
			while len(musicQue) >= 0:
				yield from asyncio.sleep(2)
				try:	
					if player.is_done():
						if len(musicQue) == 0:
							player = None
							yield from voice.disconnect()
							voice = None
							break
						else:
							yield from playmusicque(voice, musicQue[0])
							break
				except:
					pass

		elif message.content.startswith("!yt") and len(message.content.split()) != 2:
			yield from client.send_message(message.channel, 'You must have a youtube url to show, has to be the last part after v=')
	elif message.content.lower().startswith('!skillbuilds') or message.content.lower().startswith('!t5skillbuilds'):
			if message.content.lower().startswith('!skillbuilds'):
				dnClass = message.content.lower().replace('!skillbuilds ', '')
			elif message.content.lower().startswith('!t5skillbuilds'):
				dnClass = message.content.lower().replace('!t5skillbuilds ', '')
			if '!skillbuilds' == str(message.content).lower() or '!skillbuilds ' == str(message.content).lower():
				yield from client.send_message(message.channel, 'http://dnmaze.com/')
			elif '!t5skillbuilds' == str(message.content).lower() or '!t5skillbuilds ' == str(message.content).lower():
				yield from client.send_message(message.channel, 'https://dnss-kr.herokuapp.com/')
			else:
				try:
					if message.content.lower().startswith('!skillbuilds'):
						yield from client.send_message(message.channel, 'http://dnmaze.com/'+MainResponses["dnskillbuilds"][dnClass])
					elif message.content.lower().startswith('!t5skillbuilds'):
						yield from client.send_message(message.channel, 'https://dnss-kr.herokuapp.com/'+MainResponses["t5dnskillbuilds"][dnClass])
				except:
					yield from client.send_message(message.channel, '2nd argument not recognised')

	elif message.content.startswith("!voiceid"):
		yield from client.send_message(message.channel, message.author.voice_channel.id)


@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	yield from client.change_status(game=discord.Game(name='as hitler'))

def main_task():
	yield from client.login(dLogin['username'], dLogin['password'])
	yield from client.connect()


loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(main_task())
except Exception:
	loop.run_until_complete(client.close())
finally:
	loop.close()
