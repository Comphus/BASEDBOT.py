import discord
import asyncio
from datetime import datetime
import requests
import json
import fileinput
import io
import os
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


qQuestion = ['should','can','will','may','are','might','is','do','would','was','am','?','did','how']
magicEight = ['Yes','It is certain','It is decidedly so','Without a doubt','Yes, definitely','You may rely on it','As I see it, yes','Most likely','Outlook good','Signs point to a yes','Reply hazy try again','Ask again later','Better not tell you now','Cannot predict now','Concentrate and ask again','Don\'t count on it','My reply is no','My sources say no','Outlook not so good','Very doubtful']
twitchEmotes = []
MainResponses = {}
dLogin={}
voice = None
player = None
musicQue = []
currentsong = ''
timeoutStore = 0
powerTimeout = {}
dTimeout = {}
counts1 = 0
countsBNS = 0
tCounter = False
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

"""
@client.async_event
def on_member_remove:
	128685366935945217
	"""


@client.async_event
def on_message(message):
	global timeoutStore
	global powerTimeout
	global voice
	global player
	global musicQue
	global currentsong
	global counts1
	global dTimeout
	global countsBNS
	global tCounter
	global qQuestion
	global magicEight
	cTime = datetime.now()
	wtfyousay = """
	What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo.
	"""

	if client.user == message.author:
		return
	
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
			"""
	if message.content.startswith('!timeout') and str(message.author.id) in dAdmins and len(message.content.split()) == 3 and type(int(message.content.split()[2])) == type(1):
		newM = message.content.split()
		powerTimeout[newM[1]] = [int(newM[2]),0,message.mentions[0]]
		yield from client.add_roles(message.mentions[0], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
		yield from client.send_message(message.channel, newM[1]+' has been timed out for '+newM[2]+' seconds.')
		yield from asyncio.sleep(powerTimeout[newM[1]][0])
		try:
			client.remove_roles(powerTimeout[i][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
		except:
			pass
		try:
			powerTimeout.pop(i)
		except:
			pass
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
		
	if len(message.content) > 0 and message.channel.is_private == False and message.author.mention() not in powerTimeout.keys() and str(message.author.id) != '106469383206883328':
		mId = str(message.author.id)
		if mId in dTimeout:






	if str(message.author.id) not in dTimeout:
		dTimeout[str(message.author.id)] = [0,0,0]
		"""

	if message.content.startswith('!') == False:
		for t in twitchEmotes:
			if t in message.content:
				yield from client.send_file(message.channel, 'C:/DISCORD BOT/twitch emotes/'+t+'.jpg')
				break
	elif message.content.lower().split()[0] in MainResponses['all!commands']:
		yield from client.send_message(message.channel, MainResponses['all!commands'][message.content.lower().split()[0]])


		
	if message.content.startswith('!vanish') and len(message.content.split()) == 3 and message.author.id in dMods and type(1) == type(int(message.content.split()[2])) and len(message.mentions) > 0:
		logs = yield from client.logs_from(message.channel, limit=int(message.content.split()[2]))
		for log in logs:
			if log.author.mention == message.mentions[0].mention:
				yield from client.delete_message(log)
		with io.open('vanishlog.txt','a',encoding='utf-8') as f:
			s = ('Name: ' +str(message.author.name)+ ' ID:' + str(message.author.id)+ ' What they wrote:' + str(message.content)+ '\n')
			f.write(s)
	elif message.content.startswith('!vanish') and len(message.content.split()) != 3:
		yield from client.send_message(message.channel, 'The format for !vanish is: "!vanish (@mention to person) (number of messages to delete)" and is only accessable to chatmods and above.')
		
	if message.content in unicodeResponses:
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
			if guess and answer in guess.content.lower():
				yield from client.send_message(message.channel, 'Congratulations {}! You\'ve won!'.format(guess.author.mention))
				return
	if message.channel.server.id == '106293726271246336':
		with io.open('chatLogs.txt','a',encoding='utf-8') as f:
			logT = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
			logM = (str(message.author)+'('+str(message.author.id)+') '+ logT +': '+str(message.content)+'\n')
			f.write(logM)
		if message.content.startswith('!chatlogs') and message.author.id in dAdmins and message.channel.id == '106301620500836352':
			yield from client.send_file(message.channel, 'chatLogs.txt')
		if message.content.startswith("!yt") and len(message.content.split()) == 2:
			if voice == None:
				voice = yield from client.join_voice_channel(message.author.voice_channel)
				#voice = yield from client.join_voice_channel(discord.utils.get(client.get_all_channels(), id ='129079702403940352'))
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
			if 'pause' in message.content and player != None:
				if voice.is_connected():
					player.pause()
			if 'resume' in message.content and player != None:
				if voice.is_connected():
					player.resume()
			musicControls = ["next", "list", "song","pause", "resume"]
			if 'list' in message.content and player != None and len(musicQue) >0:
				returnS = ''
				for i in musicQue:
					if i not in musicControls:
						returnS += ('www.youtube.com/watch?v='+i+'\n')
				yield from client.send_message(message.channel, 'Current list of music in queue\n\n'+returnS)
				returnS = ''
			if 'song' in message.content and player != None and len(musicQue) >0:
				print(currentsong)
				yield from client.send_message(message.channel, 'Current song playing: '+ currentsong)
			def playmusicque(voice, queurl):
				global player
				global currentsong
				try:
					if queurl == "next" or queurl == "list" or queurl == "song" or queurl == "pause" or queurl == "resume":
						musicQue.pop(0)
						pass
					elif player != None:
						player.stop()
						player = voice.create_ytdl_player('https://www.youtube.com/watch?v='+queurl)
						player.start()
						currentsong = ('https://www.youtube.com/watch?v='+queurl)
						if 'youtube' not in musicQue[0]:
							yield from client.send_message(message.channel, 'currently playing: https://www.youtube.com/watch?v='+musicQue[0])
						else:
							yield from client.send_message(message.channel, 'currently playing: '+ musicQue[0])
						musicQue.pop(0)
					else:
						player = voice.create_ytdl_player('https://www.youtube.com/watch?v='+queurl)
						player.start()
						currentsong = ('https://www.youtube.com/watch?v='+queurl)
						if 'youtube' not in musicQue[0]:
							yield from client.send_message(message.channel, 'currently playing: https://www.youtube.com/watch?v='+musicQue[0])
						else:
							yield from client.send_message(message.channel, 'currently playing: '+ musicQue[0])
						musicQue.pop(0)
				except Exception as e:
					musicQue.pop(0)
					yield from client.send_message(message.channel, e)
			if player == None:
				if len(musicQue) == 1:
					yield from playmusicque(voice, musicQue[0])
			while len(musicQue) >= 0:
				yield from asyncio.sleep(2)
				print("hello1")
				try:    
					if player.is_done():
						print("hello2")
						if len(musicQue) == 0:
							yield from client.send_message(message.channel, "No more songs in queue")
							player = None
							yield from voice.disconnect()
							voice = None
							break
						else:
							print("hello4")
							yield from playmusicque(voice, musicQue[0])
							break
				except:
					pass




		elif message.content.startswith("!yt") and len(message.content.split()) != 2:
			yield from client.send_message(message.channel, 'You must have a youtube url to show, has to be the last part after v=')

	if message.content.lower().startswith('!skillbuilds') or message.content.lower().startswith('!t5skillbuilds'):
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
	if message.content.startswith("!xD"):
		yield from client.send_message(message.channel, """
X               X      DDDDD
   X         X         D            D
	   X X             D              D
	   X X             D              D
	X        X         D             D
X                X     DDDDD
															""")
		"""
	if str(message.content).count('┻') > 1:
		t = int(str(message.content).count('┻')/2)
		yield from client.send_message(message.channel, '┬─┬ ノ( ^_^ノ) '* t)
		"""
	#if message.content.startswith('O') and message.content.endswith('O') and 'u' in message.content.lower():
	#	yield from client.delete_message(message)
	if message.content.startswith('!define') and len(message.content.split()) > 1:
		words = message.content[8:]
		r = requests.get('http://api.urbandictionary.com/v0/define?term=' + words)
		tData = r.json()
		if r.status_code == 200:
			try:
				if True:
					tCounter = True
					i = random.randint(0, len(tData['list'])-1)
					dWord = tData['list'][i]['word']
					dDef = tData['list'][i]['definition']
					dEx = tData['list'][i]['example']
					yield from client.send_message(message.channel, "__Word__: {}\n__**Definition**__\n{}".format(dWord,dDef,dEx))
				else:
					yield from client.send_message(message.channel, "on cd")
			except:
				yield from client.send_message(message.channel, 'Word is not defined')
		else:
			yield from client.send_message(message.channel, 'something went wrong :(')
	elif message.content.startswith('!define') and len(message.content.split()) == 1:
		yield from client.send_message(message.channel, 'need something to define')
	if message.content.startswith('!spookme'):
		skeleR = random.randint(0,39)
		if skeleR <=30:
			yield from client.send_message(message.channel, message.author.mention + ' YOU\'VE BEEN SPOOKED!')
			yield from client.send_file(message.channel, 'skele'+str(skeleR)+'.jpg')
		elif skeleR <=38:
			yield from client.send_message(message.channel, message.author.mention + ' YOU\'VE BEEN SUPER SPOOKED!')
			yield from client.send_file(message.channel, 'skele'+str(skeleR)+'.jpg')
		else:
			yield from client.send_message(message.channel, 'YOU\'VE BEEN SPOOKED TO DEATH\nhttps://www.youtube.com/watch?v=O8XfV8aPAyQ')
	if message.content.startswith('!dance'):
		dancing = ['♪┏(°.°)┛♪','♪┗(°.°)┓♪','♪┗(°.°)┛♪','♪┏(°.°)┓♪']
		dance = yield from client.send_message(message.channel, 'Let\'s dance!')
		yield from asyncio.sleep(1)
		for j in range(5):
			for i in dancing:
				yield from client.edit_message(dance, i)
				yield from asyncio.sleep(0.1)
	if message.content.startswith('!checktwitch') and len(message.content.split()) == 2:
		tChan = message.content.split()[-1].lower()
		if tChan == 'jaesung':
			tChan = 'lsjjws3'
		r = requests.get('https://api.twitch.tv/kraken/streams/'+tChan)
		if r.status_code == 200:
			tData = r.json()
			if tData['stream'] == None:
				if tChan == 'jaesung':
					tChan = 'lsjjws3'
					yield from client.send_message(message.channel, tChan+'\'s channel is currently offline!')
				else:
					yield from client.send_message(message.channel, tChan+'\'s channel is currently offline!')
			else:
				if tChan == 'jaesung':
					tChan = 'lsjjws3'
					yield from client.send_message(message.channel, tChan+'\'s channel is currently online!')
					yield from client.send_message(message.channel, tChan+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+tChan))
				else:
					yield from client.send_message(message.channel, tChan+'\'s channel is currently online!')
					yield from client.send_message(message.channel, tChan+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+tChan))
		elif r.status_code == 404:
			yield from client.send_message(message.channel, 'This channel does not exist.')
		elif r.status_code == 422:
			yield from client.send_message(message.channel, 'Channel ' + tChan + ' is a justin.tv channel and doesnt work on twitch or is banned!')
	elif message.content.startswith('!checktwitch') and len(message.content.split()) == 1:
		client.send_message(message.channel, 'The format of !checktwitch is !checktwitch (channelname).')
	elif message.content.startswith('!checktwitch') and len(message.content.split()) > 2:
		client.send_message(message.channel, 'The !checktwitch function only takes 1 argument!')
	if message.content.startswith('!shoot') and len(message.content.split()) == 2:
		shooting = ['(⌐■_■)--︻╦╤─ -    ','(⌐■_■)--︻╦╤─  -   ','(⌐■_■)--︻╦╤─   -  ','(⌐■_■)--︻╦╤─    - ','(⌐■_■)--︻╦╤─     -']
		backshooting = ['    - ─╦╤︻--(■_■ㄱ)','   -  ─╦╤︻--(■_■ㄱ)','  -   ─╦╤︻--(■_■ㄱ)',' -    ─╦╤︻--(■_■ㄱ)','-     ─╦╤︻--(■_■ㄱ)']
		shootrand = random.randint(0,99)
		if len(message.mentions) > 0:
			if shootrand < 89:
				shot = yield from client.send_message(message.channel, '{} shoots {}{}'.format(message.author.mention,'(⌐■_■)--︻╦╤─-     ',message.mentions[0].mention))
				for i in shooting:
					yield from asyncio.sleep(0.1)
					yield from client.edit_message(shot, '{} shoots {}{}'.format(message.author.mention,i,message.mentions[0].mention))

			elif shootrand < 98:
				shot = yield from client.send_message(message.channel, '{}{} the tables have turned! {}'.format(message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',message.mentions[0].mention))
				for i in backshooting:
					yield from asyncio.sleep(0.1)
					yield from client.edit_message(shot, '{}{} the tables have turned! {}'.format(message.author.mention,i,message.mentions[0].mention))
			else:
				yield from client.send_message(message.channel, '{} and {} make love!'.format(message.author.mention,message.mentions[0].mention))
		elif discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members) != None:
			if shootrand < 89:
				shot = yield from client.send_message(message.channel, '{} shoots {}{}'.format(message.author.mention,'(⌐■_■)--︻╦╤─-     ',discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
				for i in shooting:
					yield from asyncio.sleep(0.1)
					yield from client.edit_message(shot, '{} shoots {}{}'.format(message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
			elif shootrand < 98:
				shot = yield from client.send_message(message.channel, '{}{} the tables have turned! {}'.format(message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
				for i in backshooting:
					yield from asyncio.sleep(0.1)
					yield from client.edit_message(shot, '{}{} the tables have turned! {}'.format(message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
			else:
				yield from client.send_message(message.channel, '{} and {} make love!'.format(message.author.mention,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()).mention, message.channel.server.members)))
	if message.content.startswith('!sometest') and len(message.content.split()) == 2:
		yield from client.send_message(message.channel, discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members))

	# discord help commands to get information from user


	if message.content.startswith("!voiceid"):
		yield from client.send_message(message.channel, message.author.voice_channel.id)
	if message.content.startswith('!id'):
		newR = message.content[4:]
		if len(message.content.split()) == 1:
			p = message.author.id
			yield from client.send_message(message.channel, p)
		else:
			if discord.utils.find(lambda m: m.name == newR, message.channel.server.members) == None:
				yield from client.send_message(message.channel, 'Person does not exist, or you tried to mention them')
			else:
				p = discord.utils.find(lambda m: m.name == newR, message.channel.server.members).id
				yield from client.send_message(message.channel, p)
	if message.content.startswith('!myinfo'):
		dRol = ''
		dCol = -1
		dCol1 = message.author.roles[0]
		dJoin = message.author.joined_at
		for i in message.author.roles:
			dRol += i.name + ', '
			if i.position > dCol:
				dCol1 = i
				dCol = i.position
		dCol2 = hex(dCol1.colour.value)
		dRol = dRol[0:-2].replace('@everyone', '@-everyone')
		if dRol.startswith(', '):
			dRol = dRol[2:]
		p = message.author
		yield from client.send_message(message.channel, '```Name: {}\nID: {}\nDiscriminator: {}\nRoles: {}\nJoin Date: {}\nName Color: {}```'.format(p,p.id,p.discriminator,dRol,dJoin,str(dCol2)))
	if message.content.startswith('!avatar'):
		newR = message.content[8:]
		if len(message.content.split()) == 1:
				p = message.author.avatar_url
				yield from client.send_message(message.channel, p)
		else:
			if discord.utils.find(lambda m: m.name == newR, message.channel.server.members) == None:
				yield from client.send_message(message.channel, 'Person does not exist, or you tried to mention them')
			else:
				p = discord.utils.find(lambda m: m.name == newR, message.channel.server.members).avatar_url
				yield from client.send_message(message.channel, p)
	if message.content.startswith('!serverpic'):
		yield from client.send_message(message.channel, message.channel.server.icon_url)
	if message.content.startswith('!changeme') and len(message.content.split()) >= 3 and (str(message.author.id) in '90886475373109248 90953831583617024 90869992689520640 90940396602953728 90847182772527104' or str(message.author.id) in dAdmins):
		# light pink FF69B4
		colorVal = message.content.split()[-1]
		roleName = message.content.replace('!changeme ', '')
		roleName = roleName.replace(' '+colorVal, '')
		print(roleName)
		print(colorVal)
		client.send_message(message.channel, 'None')
		if colorVal.startswith('0x') == False:
			yield from client.send_message(message.channel, 'Make sure to add \'0x\' infront of your hex value!')
			counts1 = 1
		elif discord.utils.find(lambda r: r.name == str(roleName), message.channel.server.roles) == None:
			yield from client.send_message(message.channel, 'Role name is invalid!')
			counts1 = 1
		elif counts1 == 0:
			yield from client.edit_role(message.channel.server, discord.utils.find(lambda r: r.name == str(roleName), message.channel.server.roles), colour=discord.Colour(int(colorVal, 16)))
			yield from client.send_message(message.channel, 'did it work')
		counts1 = 0
	elif message.content.startswith('!changeme') and len(message.content.split()) >= 3 and str(message.author.id) not in '90886475373109248 91347017103581184':
		yield from client.send_message(message.channel, 'You do not have access to this command')
	if message.content.startswith('!chid'):
		yield from client.send_message(message.channel, message.channel.id)
	if message.content.startswith('!serverid'):
		yield from client.send_message(message.channel, message.channel.server.id)


	# DN related ! commands to make the discord more integrated with dn
	#!pugs,trade,and mention will be put into 1 function since theyre practically the same thing, just different names and file names


	if message.content.startswith('!pugs') and str(message.channel.id) == '106300530548039680' and len(message.content.split()) > 1 and str(message.channel.server.id) == '106293726271246336' and message.mention_everyone == False:
		pugM = 'Topic is:\n'
		pugM += message.content[6:]
		if len(message.mentions) != 0:
			for i in message.mentions:
				pugM = pugM.replace(i.mention, '-No mentions-')
		if 'http' in pugM.lower():
			pugM = pugM.replace('http', '')
		with open('puglist.txt','r') as s:
			overC = 0
			pugMentions = []
			tempL = ''
			for line in s:
				tempL += line.replace('\n', ' ')
				if len(tempL) > 1900:
					pugMentions.append(tempL)
					tempL = ''
			pugMentions.append(tempL)
			for i in pugMentions:
				yield from client.send_message(message.channel, pugM + '\n\n' + i)
	elif message.content.startswith('!pugs') and str(message.channel.id) != '106300530548039680' and str(message.channel.server.id) == '106293726271246336':
		yield from client.send_message(message.channel, 'You can only call for pugs in the <#106300530548039680> channel.')
	elif message.content.startswith('!pugs') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
		yield from client.send_message(message.channel, 'You must have a topic to tell the people about what you are recruiting them for. It is BANNABLE if you do not have a legitamate topic on purpose.')
	elif message.content.lower().startswith('!pug') and str(message.channel.server.id) == '106293726271246336':
		pugL = ''
		with open('puglist.txt','r') as s:
			pugL = s.read()
		if message.author.mention not in pugL:
			with open('puglist.txt','a') as s:
				s.write(message.author.mention)
				s.write('\n')
				yield from client.send_message(message.channel, 'You have successfully signed up for pug mentions.')
		if message.author.mention in pugL:
			newL = []
			with open('puglist.txt','r') as s:
				for line in s:
					if message.author.mention not in line:
						newL.append(line)
			with open('puglist.txt','w') as s:
				for line in newL:    
					s.write(line)
			yield from client.send_message(message.channel, 'You have successfully removed yourself for pug mentions.')
	if message.content.startswith('!trades') and str(message.channel.id) == '106301265817931776' and len(message.content.split()) > 1 and str(message.channel.server.id) == '106293726271246336' and message.mention_everyone == False:
		tradeM = 'Topic is:\n'
		tradeM += message.content[8:]
		if len(message.mentions) != 0:
			for i in message.mentions:
				tradeM = tradeM.replace(i.mention, '-No mentions-')
		if 'http' in tradeM.lower():
			tradeM = tradeM.replace('http', '')
		with open('tradelist.txt','r') as s:
			overC = 0
			tradeMentions = []
			tempL = ''
			for line in s:
				tempL += line.replace('\n', ' ')
				if len(tempL) > 1900:
					pugMentions.append(tempL)
					tempL = ''
			tradeMentions.append(tempL)
			for i in tradeMentions:
				yield from client.send_message(message.channel, tradeM + '\n\n' + i)
	elif message.content.startswith('!trades') and str(message.channel.id) != '106301265817931776' and str(message.channel.server.id) == '106293726271246336':
		yield from client.send_message(message.channel, 'You can only call for trades in the <#106301265817931776> channel.')
	elif message.content.startswith('!trades') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
		yield from client.send_message(message.channel, 'You must have a topic to tell the people about what you want to trade. It is BANNABLE if you do not have a legitamate topic on purpose.')
	elif message.content.lower().startswith('!trade') and str(message.channel.server.id) == '106293726271246336':
		tradeL = ''
		with open('tradelist.txt','r') as s:
			tradeL = s.read()
		if message.author.mention not in tradeL:
			with open('tradelist.txt','a') as s:
				s.write(message.author.mention)
				s.write('\n')
				yield from client.send_message(message.channel, 'You have successfully signed up for trade mentions.')
		if message.author.mention in tradeL:
			newL = []
			with open('tradelist.txt','r') as s:
				for line in s:
					if message.author.mention not in line:
						newL.append(line)
			with open('tradelist.txt','w') as s:
				for line in newL:    
					s.write(line)
			yield from client.send_message(message.channel, 'You have successfully removed yourself for trade mentions.')
	if message.content.startswith('!pvping') and str(message.channel.id) == '106300621459628032' and len(message.content.split()) > 1 and str(message.channel.server.id) == '106293726271246336' and message.mention_everyone == False:
		pvpM = 'Topic is:\n'
		pvpM += message.content[8:]
		if len(message.mentions) != 0:
			for i in message.mentions:
				pvpM = pvpM.replace(i.mention, '-No mentions-')
		if 'http' in pvpM.lower():
			pvpM = pvpM.replace('http', '')
		with open('pvplist.txt','r') as s:
			overC = 0
			pvpMentions = []
			tempL = ''
			for line in s:
				tempL += line.replace('\n', ' ')
				if len(tempL) > 1900:
					pvpMentions.append(tempL)
					tempL = ''
			pvpMentions.append(tempL)
			for i in pvpMentions:
				yield from client.send_message(message.channel, pvpM + '\n\n' + i)
	elif message.content.startswith('!pvping') and str(message.channel.id) != '106300621459628032' and str(message.channel.server.id) == '106293726271246336':
		yield from client.send_message(message.channel, 'You can only call for pvp in the <#106300621459628032> channel.')
	elif message.content.startswith('!pvping') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
		yield from client.send_message(message.channel, 'You must have a topic to tell the people about your pvp request. It is BANNABLE if you do not have a legitamate topic on purpose.')
	elif message.content.lower().startswith('!pvp') and str(message.channel.server.id) == '106293726271246336':
		pvpL = ''
		with open('pvplist.txt','r') as s:
			pvpL = s.read()
		if message.author.mention not in pvpL:
			with open('pvplist.txt','a') as s:
				s.write(message.author.mention)
				s.write('\n')
				yield from client.send_message(message.channel, 'You have successfully signed up for pvp mentions.')
		if message.author.mention in pvpL:
			newL = []
			with open('pvplist.txt','r') as s:
				for line in s:
					if message.author.mention not in line:
						newL.append(line)
			with open('pvplist.txt','w') as s:
				for line in newL:    
					s.write(line)
			yield from client.send_message(message.channel, 'You have successfully removed yourself for pvp mentions.')

	elif message.content.startswith('!savednbuild'):
		print(message.content.split()[-1])
		print(message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com'))
		countsBNS = 0
		if message.content == ('!savednbuild') or message.content == ('!savednbuild ') and countsBNS == 0:
			yield from client.send_message(message.channel, 'Your build must contain the format !savednbuild $(name of command) (tree build url)')
			countsBNS = 1
		if message.content.split()[-1].startswith('https://dnss.herokuapp.com') == False and countsBNS == 0:
			if message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') == False and countsBNS == 0:
				if message.content.split()[-1].startswith('https://dnmaze.com') == False and countsBNS == 0:
					yield from client.send_message(message.channel, 'Your URL must be from dnss.herokuapp.com, dnss-kr.herokuapp.com or https://dnmaze.com or is missing the https:// prefix')
					countsBNS = 1
		if len(message.content.split()) == 2 and message.content.split()[1].startswith('$') == False and countsBNS == 0:
			yield from client.send_message(message.channel, 'Your command created command must have $ infront')
			countsBNS = 1
		if len(str(message.content).split()) !=3 and countsBNS == 0:
			yield from client.send_message(message.channel, 'Can only create a link with exactly 3 arguments')
			countsBNS = 1
		if len(message.content.split()) == 3 and '$' in message.content.split()[1] and countsBNS == 0: 
			with open('DNbuilds.txt','r+') as dnBuilds:
				for line in dnBuilds:
					if message.content.split()[1] in line:
						yield from client.send_message(message.channel, 'A build with this name already exists!')
						countsBNS = 1
		if countsBNS == 0:
			dnBuildsSave = message.content.replace('!savednbuild ', '')
			with open('DNbuilds.txt','a') as bnsBuilds2:
				bnsBuilds2.write(str(message.author.id) + ' ' + dnBuildsSave + '\n')
				yield from client.send_message(message.channel, 'build "'+message.content.split()[2]+'" saved! Use your command "'+message.content.split()[1]+'" to use it!')
		countsBNS = 0
		pmCount = 1
	elif message.content.startswith('$') and counts1 == 0:
		with open('DNbuilds.txt') as readBuilds:
			for line in readBuilds:
				if message.content.split()[0] == line.split()[-2]:
					yield from client.send_message(message.channel, line.split()[-1])
					counts1 = 1
		counts1 = 0
		pmCount = 1
	elif message.content.startswith('!mydnbuilds'):
		tempCount = 1
		with open('DNbuilds.txt') as readBuilds:
			for line in readBuilds:
				if str(message.author.id) in line or str(message.author) in line:
					yield from client.send_message(message.channel, str(tempCount)+': '+line.replace(str(message.author.id)+ ' ', ''))
					tempCount += 1
		if tempCount == 1:
			yield from client.send_message(message.channel, 'You have no saved builds!')
		pmCount = 1
	elif message.content.startswith('!editdnbuild'):
		countsBNS = 0
		if message.content == ('!editdnbuild') or message.content == ('!editdnbuild ') and countsBNS == 0:
			yield from client.send_message(message.channel, 'Your build must contain the format !editdnbuild $(name of command) (tree build url)')
			countsBNS = 1
		if message.content.split()[-1].startswith('https://dnss.herokuapp.com') == False and countsBNS == 0:
			if message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') == False and countsBNS == 0:
				if message.content.split()[-1].startswith('https://dnmaze.com') == False and countsBNS == 0:
					yield from client.send_message(message.channel, 'Your URL must be from dnss.herokuapp.com ,dnss-kr.herokuapp.com or http://dnmaze.com/ or is missing the http(s):// prefix')
					countsBNS = 1
		if len(message.content.split()) == 2 and message.content.split()[1].startswith('$') == False and countsBNS == 0:
			yield from client.send_message(message.channel, 'Your edited command must have $ infront')
			countsBNS = 1
		if len(str(message.content).split()) !=3 and countsBNS == 0:
			yield from client.send_message(message.channel, 'Can only edit a link with exactly 3 arguments')
			countsBNS = 1
		if countsBNS == 0:
			saveL = ''
			dnBuildsSave = message.content.replace('!editdnbuild ', '')
			with open('DNbuilds.txt','r') as bnsBuilds2:
				for line in bnsBuilds2:
					if message.content.split()[1] in line:
						if str(message.author.id) not in line:
							yield from client.send_message(message.channel, 'This is not your build so you cannot edit it.')
							countsBNS = 1
						elif str(message.author.id) in line:
							saveL = line.rsplit(' ', 1)[0] + ' ' + message.content.split()[-1]
			saveL += '\n'
			if countsBNS == 0:
				newLines = []
				with open('DNbuilds.txt','r') as bnsBuilds2:
					for line in bnsBuilds2:
						if message.content.split()[1] not in line:
							newLines.append(line)
						else:
							newLines.append(saveL)
				with open('DNbuilds.txt','w') as bnsBuilds2:
					for line in newLines:
						bnsBuilds2.write(line)
				yield from client.send_message(message.channel, 'build "'+message.content.split()[2]+'" has been edited! Use your command "'+message.content.split()[1]+'" to use it!')
		countsBNS = 0
		pmCount = 1
	
	elif message.content.startswith('!deletednbuild'):
		countsBNS = 0
		if message.content == ('!deletednbuild') or message.content == ('!deletednbuild ') and countsBNS == 0:
			yield from client.send_message(message.channel, 'Your build must contain the format !deletednbuild $(name of command)')
			countsBNS = 1
		if len(message.content.split()) == 2 and message.content.split()[1].startswith('$') == False and countsBNS == 0:
			yield from client.send_message(message.channel, 'Your command created command must have $ infront')
			countsBNS = 1
		if len(str(message.content).split()) !=2 and countsBNS == 0:
			yield from client.send_message(message.channel, 'Can only delete a link with exactly 2 arguments')
			countsBNS = 1
		if countsBNS == 0:
			dnBuildsSave = message.content.replace('!deletednbuild ', '')
			with open('DNbuilds.txt','r') as bnsBuilds2:
				for line in bnsBuilds2:
					if message.content.split()[1] in line:
						if str(message.author.id) not in line:
							yield from client.send_message(message.channel, 'This is not your build so you cannot delete it.')
							countsBNS = 1
			if countsBNS == 0:
				newLines = []
				with open('DNbuilds.txt','r') as bnsBuilds2:
					for line in bnsBuilds2:
						if message.content.split()[1] not in line:
							newLines.append(line)
				with open('DNbuilds.txt','w') as bnsBuilds2:
					for line in newLines:
						bnsBuilds2.write(line)
				yield from client.send_message(message.channel, 'Your build ' + message.content.split()[-1] + ' has been deleted.')

	elif message.channel.id == '107718615452618752':
		requestedBuild = []
		requestedBuilds = []
		if 'build' in message.content.lower() and '?' in message.content and len(message.content.split()) > 1:
			for i in MainResponses["t5dnskillbuilds"]:
				if i in message.content.lower():
					requestedBuild.append(MainResponses["t5dnskillbuilds"][i])
		if len(requestedBuild) == 0:
			return
		else:
			for i in requestedBuild:
				if i not in requestedBuilds:
					requestedBuilds.append(i)
			yield from client.send_message(message.channel, 'Would you like me to PM you a list of community saved builds for {}?'.format(requestedBuilds))
			resp = yield from client.wait_for_message(author=message.author)
			if 'y' not in resp.content.lower():
				yield from client.send_message(message.channel, 'ok')
				return
			else:
				pmlist = []
				noB = False
				with open('DNbuilds.txt','r') as b:
					readB = b.readlines()
					for i in requestedBuilds:
						checksB = 0
						for line in readB:
							if i in line:
								pmlist.append(line.replace(line.split()[0], discord.utils.get(message.server.members, id = line.split()[0]).name))
								checksB += 1
						if checksB == 0:
							noB = True
						checksB = 0
				if len(pmlist) == 0:
					yield from client.send_message(message.channel, 'I\'m sorry, there appears to be no build for the class(es) requested :(')
				else:
					if noB == True:
						yield from client.send_message(message.channel, 'I\'m sorry, there appears to be no build(s) made for one or more of the classes you requested :(')
					yield from client.send_message(message.channel, 'I will send you the PM now!')
					for i in pmlist:
						yield from client.send_message(message.author, i)
	if message.channel.server.id == '109902387363217408':
		if message.content.lower().startswith('!cats'):
			rcats = random.choice(os.listdir("C:/DISCORD BOT/cats"))
			yield from client.send_file(message.channel, 'C:/DISCORD BOT/cats/'+rcats)

	if message.author.id == '90886475373109248':
		if message.content.startswith('!join') and len(message.content.split()) == 2:
			try:
				yield from client.accept_invite(message.content.split()[1])
				yield from client.send_message(message.channel, 'Joined successfully!')
			except:
				yield from client.send_message(message.channel, 'didnt work :(')
		if message.content.startswith('!debug'):
			deb = message.content[7:]
			yield from client.send_message(message.channel, str(eval(deb)))
	if message.content.startswith('<@106469383206883328>'):
		if 'who are you' == str(message.content).lower().replace('<@106469383206883328>'+ ' ', '') or 'who are you?' == str(message.content).lower().replace('<@106469383206883328>'+ ' ', ''):
			yield from client.send_message(message.channel, 'I am a bot that runs on a community made python API(more info on that in bot-and-api channel) and programmed by Comphus to have functions for this discord server')
			counts1 = 1
		elif counts1 == 0:
			for word in qQuestion:
				if word in str(message.content).lower():
					yield from client.send_message(message.channel, magicEight[random.randint(0,19)]+', ' +  message.author.mention)
					counts1 = 1
					break  
		if counts1 == 1:
			counts1 = 0
		elif 'hi' in message.content or 'Hi' in message.content or 'hello' in message.content or 'Hello' in message.content:
			yield from client.send_message(message.channel, 'Hi! ' + message.author.mention)
		elif 'bye' in message.content or 'Bye' in message.content:
			yield from client.send_message(message.channel, 'Bye-Bye! ' + message.author.mention)
		elif 'i love you' in message.content or 'I love you' in message.content or '<3' in message.content:
			yield from client.send_message(message.channel, 'I love you too <3 ' + message.author.mention)
		elif 'thank' in message.content or 'Thanks' in message.content:
			yield from client.send_message(message.channel, 'You\'re welcome! ' + message.author.mention)
		elif 'fuck you' in message.content or 'Fuck you' in message.content or 'Fuck u' in message.content or 'fuck u' in message.content or '( ° ͜ʖ͡°)╭∩╮' in message.content:
			yield from client.send_message(message.channel, '( ° ͜ʖ͡°)╭∩╮ ' + message.author.mention)
		else:
			yield from client.send_message(message.channel, 'what? ' + message.author.mention)






@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	yield from client.change_status(game=discord.Game(name='you like a fiddle'))

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


