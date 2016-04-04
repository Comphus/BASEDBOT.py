import discord
import asyncio
from datetime import datetime, date, timedelta
import requests
import json
import re
#from bson import json_util
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
extraQue = []
currentsong = ''
songtoken = False
musicon = False
timeoutStore = 0
powerTimeout = {}
dTimeout = {}
counts1 = 0
countsBNS = 0
tCounter = False
slowM = False
slowT = 0
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




unicodeResponses = {'/lenny':'( ͡° ͜ʖ ͡°)','!gardenintool':'(  ′︵‵  )/','/shrug':'¯\\\\\_(ツ)\_/¯',"!donkmay":"🎊🚢💗 **DONMAYKAY**2⃣0⃣1⃣6⃣ 💗🚢🎊"}




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
	if member.server.id not in '82210263440306176 110373943822540800':
		if str(member.server.id) not in '106293726271246336 148358898024316928':
			yield from client.send_message(member.server, 'Welcome ' + member.mention + ' to the server!')
		try:
			print(member)
		except:
			pass
		t = datetime.now()
		if str(member.server.id) == '106293726271246336':
			with io.open('joinLog.txt','a',encoding='utf-8') as f:
				retS = ('Name: ' +str(member.name)+ ' ID:' + str(member.id)+ ' Time joined:' + str(t) + ' EST\n')
				f.write(retS)

"""
@client.async_event
def on_member_update(before, after):
	if before.server.id == '106293726271246336':
		if after.status == discord.Status.online:
			if before.game != after.game:
				g = {}
				with open("played.json") as j:
					g = json.load(j)
				if before.id not in g.keys():
					g[before.id] = {}
				try:
					if after.game.name not in g[before.id].keys():
						theD = {after.game.name:[str(datetime.now()), 0]}
						g[before.id].update(theD)
				except:
					if 'None' not in g[before.id].keys():
						theD = {'None': [str(datetime.now()), 0]}
						g[before.id].update(theD)
				try:
					if before.game.name in g[before.id].keys():
						d = datetime.strptime(g[before.id][before.game.name][0], "%Y-%m-%d %H:%M:%S.%f")
						tDiff = datetime.now() - d
						g[before.id][before.game.name][1] += tDiff.seconds
						#sets the game played after to have the values of the current time
						try:
							g[before.id][after.game.name][0] = str(datetime.now())
						except:
							g[before.id]['None'][0] = str(datetime.now()) 
				except:
					if 'None' in g[before.id].keys():
						d = datetime.strptime(g[before.id]['None'][0], "%Y-%m-%d %H:%M:%S.%f")
						tDiff = datetime.now() - d
						g[before.id]['None'][1] += tDiff.seconds
						#sets the game played after to have the values of the current time
						try:
							g[before.id][after.game.name][0] = str(datetime.now())
						except:
							g[before.id]['None'][0] = str(datetime.now())


				with open('played.json', 'w') as f:
					json.dump(g, f, indent = 4)
		else:
			g = {}
			with open("played.json") as j:
				g = json.load(j)
			if before.id in g.keys():
				try:
					if before.game.name in g[before.id].keys():
						d = datetime.strptime(g[before.id][before.game.name][0], "%Y-%m-%d %H:%M:%S.%f")
						tDiff = datetime.now() - d
						g[before.id][before.game.name][1] += tDiff.seconds
						try:
							g[before.id][after.game.name][0] = str(datetime.now())
						except:
							g[before.id]['None'][0] = str(datetime.now())
				except:
					if 'None' in g[before.id].keys():
						d = datetime.strptime(g[before.id]['None'][0], "%Y-%m-%d %H:%M:%S.%f")
						tDiff = datetime.now() - d
						g[before.id]['None'][1] += tDiff.seconds
						try:
							g[before.id][after.game.name][0] = str(datetime.now())
						except:
							g[before.id]['None'][0] = str(datetime.now())

				with open('played.json', 'w') as f:
					json.dump(g, f, indent = 4)
"""
"""
@client.event
async def on_message(message):
	if message.content.startswith('!vanish') and len(message.content.split()) == 3 and (message.author.id in dMods or message.author.id in '105130465039548416') and type(1) == type(int(message.content.split()[2])) and len(message.mentions) > 0:
		logs = client.logs_from(message.channel)
		counter = 0
		async for log in logs:
			if log.author.mention == message.mentions[0].mention:
				await client.delete_message(log)
				counter += 1
			if counter == int(message.content.split()[2]):
				break
		with io.open('vanishlog.txt','a',encoding='utf-8') as f:
			s = (str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))+' '+message.server.name+' '+'Name: ' +str(message.author.name)+ ' ID:' + str(message.author.id)+ ' What they wrote:' + str(message.content)+ '\n')
			f.write(s)
	elif message.content.startswith('!vanish') and len(message.content.split()) != 3:
		await client.send_message(message.channel, 'The format for !vanish is: "!vanish (@mention to person) (number of messages to delete)" and is only accessable to chatmods and above.')
"""

@client.event
async def on_message(message):
	global timeoutStore
	global powerTimeout
	global voice
	global player
	global musicQue
	global extraQue
	global songtoken
	global currentsong
	global counts1
	global dTimeout
	global countsBNS
	global tCounter
	global qQuestion
	global magicEight
	global slowM
	global slowT
	global musicon
	cTime = datetime.now()

	if client.user == message.author:
		return

	if message.content.startswith('!delete ian'):
		with codecs.open('daddy.txt','r',"utf-8") as f:
			for i in f:
				await client.send_message(message.channel, i)
				await asyncio.sleep(2)
	if message.content.startswith('!lightproc'):
		await client.send_message(message.channel, 'Buckle up!')
		await client.send_file(message.channel, 'Comphus.jpg')

	if message.content.startswith('!slowmode') and message.author.id in dMods and message.server.id in '106293726271246336 88422130479276032':
		if len(message.content.split()) > 1  and 'off' not in message.content.lower() and type(int(message.content.split()[1])) == type(5) and int(message.content.split()[1]) < 31:
			print('hello')
			slowT = int(message.content.split()[1])
		try:				
			if type(3) == int(message.content.split()[1]): 
				if int(message.content.split()[1]) > 30:
					await client.send_message(message.channel, "max limit is 30 seconds for slowmode")
					return
		except:
			pass
		if 'off' in message.content.lower():
			await client.send_message(message.channel, "slow mode is off!")
			slowM = False
			for i in message.server.members:
				for j in i.roles:
					if 'slowmode' in j.name:
						await client.remove_roles(i, discord.utils.find(lambda r: r.name == 'slowmode', message.channel.server.roles))
		elif 'on' in message.content.lower():
			if slowT > 0:
				await client.send_message(message.channel, "slow mode is on!")
			elif slowT == 0:
				await client.send_message(message.channel, "slow mode is on! Since no time interval was stated, the default of 15 seconds has been applied!")
				slowT = 15
			slowM = True
	if slowM == True and message.server.id == '106293726271246336':
		if message.author.id not in dMods:
			await client.add_roles(message.author, discord.utils.find(lambda r: r.name == 'slowmode', message.channel.server.roles))
			await asyncio.sleep(slowT)
			await client.remove_roles(message.author, discord.utils.find(lambda r: r.name == 'slowmode', message.channel.server.roles))

	if message.content.startswith('!smashthat'):
		tr = random.randint(0,1)
		await client.send_file(message.channel, 'smash{}.jpg'.format(tr))


	
	if message.content.startswith('!vanish') and len(message.content.split()) == 3 and (message.author.id in dMods or message.author.id in '105130465039548416') and type(1) == type(int(message.content.split()[2])) and len(message.mentions) > 0:
		logs = client.logs_from(message.channel)
		counter = 0
		async for log in logs:
			if log.author.mention == message.mentions[0].mention:
				await client.delete_message(log)
				counter += 1
			if counter == int(message.content.split()[2]):
				break
		with io.open('vanishlog.txt','a',encoding='utf-8') as f:
			s = (str(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))+' '+message.server.name+' '+'Name: ' +str(message.author.name)+ ' ID:' + str(message.author.id)+ ' What they wrote:' + str(message.content)+ '\n')
			f.write(s)
	elif message.content.startswith('!vanish') and len(message.content.split()) != 3:
		await client.send_message(message.channel, 'The format for !vanish is: "!vanish (@mention to person) (number of messages to delete)" and is only accessable to chatmods and above.')

	if timeoutStore > 0:
		for i in powerTimeout:
			timeDiff = cTime - powerTimeout[i][1]
			if timeDiff.seconds >= powerTimeout[i][0]:
				await client.remove_roles(powerTimeout[i][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
				powerTimeout.pop(i)
				timeoutStore -= 1
				break
	if message.content.startswith('!timeout') and str(message.author.id) in dAdmins and len(message.content.split()) == 3 and type(int(message.content.split()[2])) == type(1):
		newM = message.content.split()
		t1 = datetime.now()
		powerTimeout[newM[1]] = [int(newM[2]),t1,message.mentions[0]]
		timeoutStore += 1
		await client.add_roles(message.mentions[0], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
		await client.send_message(message.channel, newM[1]+' has been timed out for '+newM[2]+' seconds.')
	elif message.content.startswith('!timeout') and str(message.author.id) in dAdmins:
		await client.send_message(message.channel, 'The format for timing someone out is !timeout @ mention (timeinseconds)')
	if message.content.startswith('!stoptimeout') and str(message.author.id) in dAdmins and len(message.content.split()) == 2:
		newM = message.content.split()
		if newM[1] in powerTimeout:
			await client.remove_roles(powerTimeout[newM[1]][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
			powerTimeout.pop(newM[1])
			await client.send_message(message.channel, newM[1]+'\'s timeout has been manually stopped.')
		elif 'Jail' in discord.utils.find(lambda m: m.name == 'Jail', message.channel.server.members).roles:
			await client.remove_roles(powerTimeout[newM[1]][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
			await client.send_message(message.channel, newM[1]+'\'s timeout has been manually stopped.')
		else:
			await client.send_message(message.channel, 'That person has not been manually timed out.')

	if message.content.startswith('!') == False and message.server.id != '110373943822540800':
		for t in twitchEmotes:
			if t in message.content:
				await client.send_file(message.channel, 'C:/DISCORD BOT/twitch emotes/'+t+'.jpg')
				break
	elif message.content.lower().split()[0] in MainResponses['all!commands']:
		await client.send_message(message.channel, MainResponses['all!commands'][message.content.lower().split()[0]])
		return


	"""
	if message.content.lower().startswith('.ahh'):
		logs = await client.logs_from(message.channel, limit=20)
		counter = 0
		for log in logs:
			if log.author == message.author:
				await client.delete_message(log)
				counter += 1d
			if counter == 4:
				break
	"""
		
		
	if message.content in unicodeResponses:
		await client.send_message(message.channel, unicodeResponses[message.content.lower().split()[0]])
	elif message.content.startswith('!sleep'):
		await asyncio.sleep(5)
		await client.send_message(message.channel, 'Done sleeping')
	elif message.content.startswith('!hello'):
		await client.send_message(message.channel, 'hi')
	elif message.content.startswith('!duel') and str(message.channel.id) not in '91518345953689600 106293726271246336':    
		results = dueling([message.mentions[0].mention,message.mentions[1].mention])
		await client.send_message(message.channel, results[1])
		for i in range(len(results[0])):
			await client.send_message(message.channel, results[0][i])
		await client.send_message(message.channel, results[2])
	elif message.content.startswith('!trivia') and message.channel.id != '106293726271246336':
		TriviaQuestions = MainResponses['Trivia']
		TriviaQuestion = random.choice(list(TriviaQuestions.keys()))
		await client.send_message(message.channel, 'You have started DN Trivia!\n')
		await asyncio.sleep(1)
		await client.send_message(message.channel, 'You will recieve a question and everyone has 15 seconds to answer it, so be quick! The question is:\n')
		await asyncio.sleep(3)
		await client.send_message(message.channel, TriviaQuestion)
		answer = MainResponses['Trivia'][TriviaQuestion]
		end_time = time.time() + 15
		while True:
			time_remaining = end_time - time.time()
			if time_remaining <= 0:
				await client.send_message(message.channel, 'Sorry, you took too long! The answer was '+answer)
				return
			guess = await client.wait_for_message(timeout = time_remaining)
			if guess and answer in guess.content.lower():
				await client.send_message(message.channel, 'Congratulations {}! You\'ve won!'.format(guess.author.mention))
				return
	if message.channel.server.id == '106293726271246336':
		with io.open('chatLogs.txt','a',encoding='utf-8') as f:
			logT = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
			logM = (str(message.author)+'('+str(message.author.id)+') '+ logT +': '+str(message.content)+'\n')
			f.write(logM)
		if message.content.startswith('!chatlogs') and message.author.id in dAdmins and message.channel.id == '106301620500836352':
			await client.send_file(message.channel, 'chatLogs.txt')
		if message.content.startswith("!evlogs") and message.author.id in dAdmins and message.channel.id == '106301620500836352':
			await client.send_file(message.channel, 'eventlist.txt')
		if message.content.lower().startswith('!event'):
			tradeL = ''
			with open('eventlist.txt','r') as s:
				tradeL = s.read()
			if message.author.mention not in tradeL:
				with open('eventlist.txt','a') as s:
					s.write(message.author.mention)
					s.write('\n')
					await client.send_message(message.channel, 'You have successfully signed up for Events!')
			if message.author.mention in tradeL:
				newL = []
				with open('eventlist.txt','r') as s:
					for line in s:
						if message.author.mention not in line:
							newL.append(line)
				with open('eventlist.txt','w') as s:
					for line in newL:    
						s.write(line)
				await client.send_message(message.channel, 'You have successfully removed yourself for Events!')
		if message.content.startswith("!yt") and len(message.content.split()) == 2:
			ctrC = message.content.lower().split()[1]
			musicControls = ["next", "skip", "list", "song","pause", "resume", "help"]
			if voice == None:
				try:
					voice = await client.join_voice_channel(message.author.voice_channel)
				except:
					await client.send_message(message.channel, "You are not in a voice channel, please join a voice channel in order to play music.")
					return
				#voice = await client.join_voice_channel(discord.utils.get(client.get_all_channels(), id ='129079702403940352'))
			if 'stop' in message.content:
				if voice.is_connected():
					await voice.disconnect()
					musicQue = []
					player = None
					voice = None
					songtoken = False
					return
			if ('next' in message.content or 'skip' in message.content) and player != None:
				if voice.is_connected():
					player.stop()
					if len(musicQue) == 0:
						await voice.disconnect()
						musicQue = []
					return
			if 'pause' in message.content and player != None:
				if voice.is_connected():
					player.pause()
					return
			if 'resume' in message.content and player != None:
				if voice.is_connected():
					player.resume()
					return
			if 'list' in message.content and player != None and len(musicQue) >0:
				returnS = ''
				for i in musicQue:
					if i not in musicControls:
						returnS += (i+'\n')
				await client.send_message(message.channel, 'Current list of music in queue\n\n'+returnS)
				returnS = ''
			if 'song' in message.content and player != None and len(musicQue) >0:
				await client.send_message(message.channel, 'Current song playing: **'+ player.title+'**')
			if 'help' in message.content:
				await client.send_message(message.channel, 'How to make the !yt function work, type in \'!yt \', then whatever url you want afterwards to make it play its audio, will not play from ALL links.\n__Commands you can put in after !yt for !yt are:__\n**next/skip** - goes to the next song, if there isnt one then the bot leaves\n**list** - a list of songs in queue\n**song** - current song playing\n**pause/resume** - pauses or resumes the song\n**help** - pulls up this text')
				if player == None:
					await voice.disconnect()
			async def playmusicque(voice, queurl):
				global musicon
				global player
				#global voice
				global currentsong
				global songtoken
				global extraQue
				try:
					if player != None:
						player.stop()
						player = await voice.create_ytdl_player(queurl)
						player.start()
						musicQue.pop(0)
						currentsong = (player.title)
						await client.send_message(message.channel, '**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(player.title, player.views, player.likes, player.dislikes))
						return
					else:
						player = await voice.create_ytdl_player(queurl)
						player.start()
						musicQue.pop(0)
						currentsong = (player.title)
						await client.send_message(message.channel, '**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(player.title, player.views, player.likes, player.dislikes))
						return
				except Exception as e:
					musicQue.pop(0)
					await client.send_message(message.channel, e)
					return

			if ctrC not in musicControls:
				endurl = message.content.split()[1]
				musicQue.append(endurl)
				#the loop
				if songtoken == False:
					songtoken = True
					while len(musicQue) >= 0:
						if player == None:
							print('anothertest')
							if len(musicQue) == 1:
								await playmusicque(voice, musicQue[0])
						await asyncio.sleep(2)
						print(musicQue)
						print("hello1")
						try:
							if player.is_done():
								print("hello2")
								if len(musicQue) == 0:
									await client.send_message(message.channel, "No more songs in queue")
									player = None
									await voice.disconnect()
									voice = None
									songtoken = False
									#print(songtoken)
									#break
								elif len(musicQue) > 0:
									#songtoken = True
									print("hello4")
									await playmusicque(voice, musicQue[0])
									#break
							
						except:
							pass
						
						
						try:
							if len(musicQue) == 0 and player.is_done():
								break
						except:
							pass
						if len(musicQue) == 0 and player == None:
							break
		elif message.content.startswith("!yt") and len(message.content.split()) != 2:
			await client.send_message(message.channel, 'You must have a link to show after !yt. It can be almost anything, youtube, soundcloud, even pornhub!')

	if message.content.lower().startswith('!skillbuilds') or message.content.lower().startswith('!t5skillbuilds'):
			if message.content.lower().startswith('!skillbuilds'):
				dnClass = message.content.lower().replace('!skillbuilds ', '')
			elif message.content.lower().startswith('!t5skillbuilds'):
				dnClass = message.content.lower().replace('!t5skillbuilds ', '')
			if '!skillbuilds' == str(message.content).lower() or '!skillbuilds ' == str(message.content).lower():
				await client.send_message(message.channel, 'http://dnmaze.com/')
			elif '!t5skillbuilds' == str(message.content).lower() or '!t5skillbuilds ' == str(message.content).lower():
				await client.send_message(message.channel, 'https://dnss-kr.herokuapp.com/job/')
			else:
				try:
					if message.content.lower().startswith('!skillbuilds'):
						await client.send_message(message.channel, 'http://dnmaze.com/'+MainResponses["dnskillbuilds"][dnClass])
					elif message.content.lower().startswith('!t5skillbuilds'):
						await client.send_message(message.channel, 'https://dnss-kr.herokuapp.com/job/'+MainResponses["t5dnskillbuilds"][dnClass])
				except:
					await client.send_message(message.channel, '2nd argument not recognised')
	if message.content.startswith("!xD"):
		await client.send_message(message.channel, """
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
		await client.send_message(message.channel, '┬─┬ ノ( ^_^ノ) '* t)
		"""
	#if message.content.count('O') > 1 and 'u' in message.content.lower():
	#	await client.delete_message(message)
	if message.content.startswith('!define') and len(message.content.split()) > 1 and message.channel.id != '106293726271246336':
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
					await client.send_message(message.channel, "__Word__: {}\n__**Definition**__\n{}".format(dWord,dDef,dEx))
				else:
					await client.send_message(message.channel, "on cd")
			except:
				await client.send_message(message.channel, 'Word is not defined')
		else:
			await client.send_message(message.channel, 'something went wrong :(')
	elif message.content.startswith('!define') and len(message.content.split()) == 1 and message.channel.id != '106293726271246336':
		await client.send_message(message.channel, 'need something to define')
	if message.content.startswith('!spookme'):
		skeleR = random.randint(0,39)
		if skeleR <=30:
			await client.send_message(message.channel, message.author.mention + ' YOU\'VE BEEN SPOOKED!')
			await client.send_file(message.channel, 'skele'+str(skeleR)+'.jpg')
		elif skeleR <=38:
			await client.send_message(message.channel, message.author.mention + ' YOU\'VE BEEN SUPER SPOOKED!')
			await client.send_file(message.channel, 'skele'+str(skeleR)+'.jpg')
		else:
			await client.send_message(message.channel, 'YOU\'VE BEEN SPOOKED TO DEATH\nhttps://www.youtube.com/watch?v=O8XfV8aPAyQ')
	if message.content.startswith('!dance'):
		dancing = ['♪┏(°.°)┛♪','♪┗(°.°)┓♪','♪┗(°.°)┛♪','♪┏(°.°)┓♪']
		dance = await client.send_message(message.channel, 'Let\'s dance!')
		await asyncio.sleep(1)
		for j in range(5):
			for i in dancing:
				await client.edit_message(dance, i)
				await asyncio.sleep(0.1)
	if message.content.startswith('!vladme'):
		await client.send_message(message.channel, "http://i.imgur.com/wkI7NZB.png")
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
					await client.send_message(message.channel, tChan+'\'s channel is currently offline!')
				else:
					await client.send_message(message.channel, tChan+'\'s channel is currently offline!')
			else:
				if tChan == 'jaesung':
					tChan = 'lsjjws3'
					await client.send_message(message.channel, tChan+'\'s channel is currently online!')
					await client.send_message(message.channel, tChan+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+tChan))
				else:
					await client.send_message(message.channel, tChan+'\'s channel is currently online!')
					await client.send_message(message.channel, tChan+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+tChan))
		elif r.status_code == 404:
			await client.send_message(message.channel, 'This channel does not exist.')
		elif r.status_code == 422:
			await client.send_message(message.channel, 'Channel ' + tChan + ' is a justin.tv channel and doesnt work on twitch or is banned!')
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
				shot = await client.send_message(message.channel, '{} shoots {}{}'.format(message.author.mention,'(⌐■_■)--︻╦╤─-     ',message.mentions[0].mention))
				for i in shooting:
					await asyncio.sleep(0.1)
					await client.edit_message(shot, '{} shoots {}{}'.format(message.author.mention,i,message.mentions[0].mention))

			elif shootrand < 98:
				shot = await client.send_message(message.channel, '{}{} the tables have turned! {}'.format(message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',message.mentions[0].mention))
				for i in backshooting:
					await asyncio.sleep(0.1)
					await client.edit_message(shot, '{}{} the tables have turned! {}'.format(message.author.mention,i,message.mentions[0].mention))
			else:
				await client.send_message(message.channel, '{} and {} make love!'.format(message.author.mention,message.mentions[0].mention))
		elif discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members) != None:
			if shootrand < 89:
				shot = await client.send_message(message.channel, '{} shoots {}{}'.format(message.author.mention,'(⌐■_■)--︻╦╤─-     ',discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
				for i in shooting:
					await asyncio.sleep(0.1)
					await client.edit_message(shot, '{} shoots {}{}'.format(message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
			elif shootrand < 98:
				shot = await client.send_message(message.channel, '{}{} the tables have turned! {}'.format(message.author.mention,'    - ─╦╤︻--(■_■ㄱ)',discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
				for i in backshooting:
					await asyncio.sleep(0.1)
					await client.edit_message(shot, '{}{} the tables have turned! {}'.format(message.author.mention,i,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members).mention))
			else:
				await client.send_message(message.channel, '{} and {} make love!'.format(message.author.mention,discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()).mention, message.channel.server.members)))
	if message.content.startswith('!sometest') and len(message.content.split()) == 2:
		await client.send_message(message.channel, discord.utils.find(lambda m: m.name.lower().startswith(message.content.split()[1].lower()), message.channel.server.members))
	if message.content.startswith('!gimmepoutine'):
		await client.send_file(message.channel, 'poutine.jpg')
	if message.content.lower().startswith('!mal') and len(message.content) > 5:
		import xml.etree.ElementTree as ET
		anime = message.content.lower()[5:]
		r = requests.get('http://myanimelist.net/api/anime/search.xml?q=' + anime, auth=(dLogin['maluser'], dLogin['malpassword']))
		if r.status_code == 200:
			resp = r.text
			aUrl = 'http://myanimelist.net/anime/' + re.search("id>(\d+)</i", resp).group(1)
			try:
				aName = re.search("english>(\D+)</e", resp).group(1)
			except:
				aName = None
			try:
				aJp = re.search("title>(\D+)</t", resp).group(1)
			except:
				aJp = None
			aScore = re.search("score>(\S+|\s+)</s", resp).group(1)
			aEp = re.search("episodes>(\d+)</e", resp).group(1)
			aStat = re.search("status>(\D+)</s", resp).group(1)
			aDate = re.search("start_date>(\S+|\s+)</start_date", resp).group(1)
			try:
				aDesc = re.search("synopsis>(\S+|\s+)</synopsis", resp).group(1).replace('&mdash;','—').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('<br />', '').replace('[i]', '').replace('[/i]', '')
			except:
				try:
					root = ET.fromstring(resp)[0]
					aDesc = root[10].text.replace('&amp;','&').replace('&mdash;','—').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#039;',"'").replace('<br />', '').replace('[i]', '').replace('[/i]', '')
				except:
					aDesc = None
			await client.send_message(message.channel, "**Name: **{}\n**Eng Name: **{}\n**Status: **{}\n**Air Date: **{}\n**Episodes: **{}\n**Score: **{}\n**Description: **{}\n**Link: **{}".format(aJp,aName,aStat,aDate,aEp,aScore,aDesc,aUrl))
		elif r.status_code == 204:
			await client.send_message(message.channel, "I couldnt find an anime with that name in MyAnimeList")
		else:
			await client.send_message(message.channel, "MyAnimeList is down, NOOOOOOOO :(")

	# discord help commands to get information from user

	if message.content.startswith('!totalmem'):
		await client.send_message(message.channel, "**Total Members:** {}".format(message.channel.server.member_count))
	if message.content.startswith("!voiceid"):
		await client.send_message(message.channel, message.author.voice_channel.id)
	if message.content.startswith('!id'):
		newR = message.content[4:]
		if len(message.content.split()) == 1:
			p = message.author.id
			await client.send_message(message.channel, p)
		else:
			if discord.utils.find(lambda m: m.name == newR, message.channel.server.members) == None:
				await client.send_message(message.channel, 'Person does not exist, or you tried to mention them')
			else:
				p = discord.utils.find(lambda m: m.name == newR, message.channel.server.members).id
				await client.send_message(message.channel, p)
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
		await client.send_message(message.channel, '```Name: {}\nID: {}\nDiscriminator: {}\nRoles: {}\nJoin Date: {}\nName Color: {}```'.format(p,p.id,p.discriminator,dRol,dJoin,str(dCol2)))
	if message.content.startswith('!info') and len(message.content.split()) > 1:
		dRol = ''
		dCol = -1
		p = discord.utils.find(lambda m: m.name == message.content[6:], message.channel.server.members)
		dCol1 = p.roles[0]
		dJoin = p.joined_at
		for i in p.roles:
			dRol += i.name + ', '
			if i.position > dCol:
				dCol1 = i
				dCol = i.position
		dCol2 = hex(dCol1.colour.value)
		dRol = dRol[0:-2].replace('@everyone', '@-everyone')
		if dRol.startswith(', '):
			dRol = dRol[2:]
		await client.send_message(message.channel, '```Name: {}\nID: {}\nDiscriminator: {}\nRoles: {}\nJoin Date: {}\nName Color: {}```'.format(p,p.id,p.discriminator,dRol,dJoin,str(dCol2)))

	if message.content.startswith('!avatar'):
		newR = message.content[8:]
		if len(message.mentions) > 0:
			await client.send_message(message.channel, message.mentions[0].avatar_url)
			return
		if len(message.content.split()) == 1:
				p = message.author.avatar_url
				await client.send_message(message.channel, p)
		else:
			if discord.utils.find(lambda m: m.name == newR, message.channel.server.members) == None:
				await client.send_message(message.channel, 'Person does not exist')
			else:
				p = discord.utils.find(lambda m: m.name == newR, message.channel.server.members).avatar_url
				await client.send_message(message.channel, p)
	if message.content.startswith('!serverpic'):
		await client.send_message(message.channel, message.channel.server.icon_url)
	if message.content.startswith('!changeme') and len(message.content.split()) >= 3 and (str(message.author.id) in '90910424551145472 90886475373109248 90953831583617024 90869992689520640 90940396602953728 90847182772527104' or str(message.author.id) in dAdmins):
		# light pink FF69B4
		colorVal = message.content.split()[-1]
		roleName = message.content.replace('!changeme ', '')
		roleName = roleName.replace(' '+colorVal, '')
		print(roleName)
		print(colorVal)
		client.send_message(message.channel, 'None')
		if colorVal.startswith('0x') == False:
			await client.send_message(message.channel, 'Make sure to add \'0x\' infront of your hex value!')
			counts1 = 1
		elif discord.utils.find(lambda r: r.name == str(roleName), message.channel.server.roles) == None:
			await client.send_message(message.channel, 'Role name is invalid!')
			counts1 = 1
		elif counts1 == 0:
			await client.edit_role(message.channel.server, discord.utils.find(lambda r: r.name == str(roleName), message.channel.server.roles), colour=discord.Colour(int(colorVal, 16)))
			await client.send_message(message.channel, 'did it work')
		counts1 = 0
	elif message.content.startswith('!changeme') and len(message.content.split()) >= 3 and str(message.author.id) not in '90886475373109248 91347017103581184':
		await client.send_message(message.channel, 'You do not have access to this command')
	if message.content.startswith('!chid'):
		await client.send_message(message.channel, message.channel.id)
	if message.content.startswith('!serverid'):
		await client.send_message(message.channel, message.channel.server.id)

	#BNS commands
	if message.content.startswith('!bnstree'):
		bnsClass = message.content.replace('!bnstree ', '').lower()
		if '!bnstree' == message.content:
			await client.send_message(message.channel, 'https://bnstree.com/')
			return
		elif 'blade master' == bnsClass or 'bm' == bnsClass:
			await client.send_message(message.channel, 'https://bnstree.com/BM')
			return
		elif 'kfm' == bnsClass or 'kungfu master' == bnsClass or 'kung fu master' == bnsClass or 'kungfumaster' == bnsClass or 'kf' == bnsClass:
			await client.send_message(message.channel, 'https://bnstree.com/KF')
			return
		elif 'destroyer' == bnsClass or 'des' == bnsClass or 'de' == bnsClass or 'destro' == bnsClass or 'dest' == bnsClass:
			await client.send_message(message.channel, 'https://bnstree.com/DE')
			return
		elif 'force master' == bnsClass or 'fm' == bnsClass or 'forcemaster' == bnsClass or 'force user' == bnsClass:
			await client.send_message(message.channel, 'https://bnstree.com/FM')
			return
		elif 'assassin' == bnsClass or 'as' == bnsClass or 'sin' == bnsClass:
			await client.send_message(message.channel, 'https://bnstree.com/AS')
			return
		elif 'summoner' == bnsClass or 'su' == bnsClass or 'summ' == bnsClass or 'sum' == bnsClass:
			await client.send_message(message.channel, 'https://bnstree.com/SU')
			return
		elif 'blade dancer' == bnsClass or 'bd' == bnsClass or 'bladedancer' == bnsClass or 'lbm' == bnsClass or 'lyn blade master' == bnsClass or 'lynblade master' == bnsClass or 'lyn blademaster' == bnsClass:
			await client.send_message(message.channel, 'https://bnstree.com/BD')
			return
		elif 'warlock' == bnsClass or 'wl' == bnsClass or 'lock' == bnsClass:
			await client.send_message(message.channel, 'https://bnstree.com/WL')
			return
		else:
			await client.send_message(message.channel, '2nd argument not recognised')
			return
		
	if message.content.startswith('!testbns'):
		await client.send_message(message.channel, "http://na-bns.ncsoft.com/ingame/bs/character/duel?c=Taichou\nhttp://na-bns.ncsoft.com/web/ingame/character/favorcharacter.jsp\nhttp://na-bns.ncsoft.com/web/ingame/character/a_duelinfo.jsp")
	if message.content.lower().startswith('!bns') and len(message.content.split()) > 1 and message.channel.id != '106293726271246336 88422130479276032 124934505810100224 146298657765851137 144803652635328512':
		newM = message.content.lower()[5:]
		newerM = newM.split()
		if len(newerM) > 1:
			newestM = '%20'.join(newerM)
		else:
			newestM = newerM[0]
		if "faggot" in newestM.lower():
			await client.send_message(message.channel, 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c=Rain')
			await client.send_message(message.channel, 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c=Minko')
			return
		r = requests.get('http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+newestM)
		if len(r.history) == 0:
			await client.send_message(message.channel, 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+newestM+'&s=101')
			from bs4 import BeautifulSoup
			soup = BeautifulSoup(r.text, 'html.parser')
			#print(soup.find_all("div", class_="charaterView")[0].img['src'])
			#print(soup.find_all(attrs={"class":"signature"})[0].find_all(attrs={"href":"#"})[0].string)#.find_all(attrs={"class":"desc"})[0])
			try:
				clan = soup.find_all(attrs={"class":"signature"})[0].find_all(attrs={"class":"guild"})[0].text
			except:
				clan = 'None'
			classname = soup.find_all(attrs={"class":"signature"})[0].find_all("ul")[0].li.string
			level = soup.find_all(attrs={"class":"signature"})[0].find_all("li")[1].text.split()[1]
			try:
				hmlevel = soup.find_all(attrs={"class":"signature"})[0].find_all("li")[1].find_all(attrs={"class":"masteryLv"})[0].string.replace("Dark Arts Level", "**Dark Arts Level:**")
			except:
				hmlevel = "**Dark Arts Level:** 0"
			att = soup.find_all("div", class_="attack")[0].span.string
			hp = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[0].find(class_="stat-point").string
			pierce = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-title"})[2].find(class_="stat-point").string
			piercep = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-description"})[2].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			defense = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[1].find(class_="stat-point").string
			defensep = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-description"})[1].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			acc = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-title"})[3].find(class_="stat-point").string
			accp = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-description"})[3].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			eva = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[3].find(class_="stat-point").string
			evap = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-description"})[3].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			chit = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-title"})[5].find(class_="stat-point").string
			chitp = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-description"})[5].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			block = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[4].find(class_="stat-point").string
			blockp = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-description"})[4].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[4].string
			cdmg = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-title"})[6].find(class_="stat-point").string
			cdmgp = soup.find_all(attrs={"class":"stat-define"})[0].find_all(attrs={"class":"stat-description"})[6].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[2].string
			critd = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-title"})[5].find(class_="stat-point").string
			critdp = soup.find_all(attrs={"class":"stat-define"})[1].find_all(attrs={"class":"stat-description"})[5].find_all(attrs={"class":"ratio"})[0].find_all(class_="stat-point")[1].string
			await client.send_message(message.channel, "**Clan:** {}\n**Class:** {}\n**Level:** {}\n{}\n**Attack:** {}                                                        **HP:** {}\n**Pierce:** {}({})                                          **Defense:** {}({})\n**Accuracy:** {}({})                                 **Evasion:** {}({})\n**Critical Hit:** {}({})                              **Block:** {}({})\n**Critical Damage** {}({})                    **Crit Defense:** {}({})".format(clan,classname,level,hmlevel,att,hp,pierce,piercep,defense,defensep,acc,accp,eva,evap,chit,chitp,block,blockp,cdmg,cdmgp,critd,critdp))
			await client.send_message(message.channel, soup.find_all("div", class_="charaterView")[0].img['src'])
			return
		else:
			await client.send_message(message.channel, 'Character name does not exist')
			return
	if message.content.startswith('!bnsdaily'):
		await client.send_file(message.channel, "bnsdailymap.png")
		return
	if message.content.startswith('!bnsbuild'):
		await client.send_message(message.channel, "https://docs.google.com/document/d/1kCNNIdKcyXL6kgrXPLJdPk-yy1oqNPrunNc8x0PP7D4/edit?pref=2&pli=1")
		return
	if message.content.startswith('!bns') and len(message.content.split()) == 1:
		await client.send_message(message.channel, 'the format for seeing a players bns info is \'!bns (player ign)\'')

	if message.content.startswith('!savebnsbuild'):
		if message.content == ('!savebnsbuild') or message.content == ('!savebnsbuild '):
			await client.send_message(message.channel, 'Your build must contain the format (!savebnsbuild !!(name of command) (tree build url)')
			countsBNS = 1
		elif message.content.split()[-1].startswith('https://bnstree.com/') == False:
			await client.send_message(message.channel, 'Your URL must be from bnstree.com or is missing the https:// prefix')
			countsBNS = 1
		elif message.content.split()[1].startswith('!!') == False:
			await client.send_message(message.channel, 'Your command created command must have !! infront')
			countsBNS = 1
		elif len(str(message.content).split()) !=3:
			await client.send_message(message.channel, 'Can only create a link with exactly 3 arguments')
			countsBNS = 1
		elif len(message.content.split()) == 3 and '!!' in message.content.split()[1]: 
			with open('BNSBuilds.txt','r+') as bnsBuilds:
				for line in bnsBuilds:
					if message.content.split()[1] in line:
						await client.send_message(message.channel, 'A build with this name already exists!')
						countsBNS = 1
		if countsBNS == 0:
			bnsBuildsSave = message.content.replace('!savebnsbuild ', '')
			with open('BNSBuilds.txt','a') as bnsBuilds2:
				bnsBuilds2.write(str(message.author.id) + ' ' + bnsBuildsSave + '\n')
				await client.send_message(message.channel, 'build "'+message.content.split()[2]+'" saved! Use your command "'+message.content.split()[1]+'" to use it!')
		countsBNS = 0
	if message.content.startswith('!!') and counts1 == 0:
		with open('BNSBuilds.txt') as readBuilds:
			for line in readBuilds:
				if message.content.split()[0] == line.split()[1]:
					await client.send_message(message.channel, line.split()[-1])
					counts1 = 1
		counts1 = 0
	
	if message.content.startswith('!mybnsbuilds'):
		tempCount = 1
		with open('BNSBuilds.txt') as readBuilds:
			for line in readBuilds:
				if str(message.author.id) in line:
					await client.send_message(message.channel, str(tempCount)+': '+line.replace(str(message.author.id)+ ' ', ''))
					tempCount += 1
		if tempCount == 1:
			await client.send_message(message.channel, 'You have no saved builds!')
	if message.content.startswith('!editbnsbuild'):
		if message.content == ('!editbnsbuild') or message.content == ('!editbnsbuild ') and countsBNS == 0:
			await client.send_message(message.channel, 'Your build must contain the format !editbnsbuild !!(name of command) (tree build url)')
			countsBNS = 1
		elif message.content.split()[-1].startswith('https://bnstree.com/') == False and countsBNS == 0:
			await client.send_message(message.channel, 'Your URL must be from dnss.herokuapp.com ,dnss-kr.herokuapp.com or http://dnmaze.com/ or is missing the http(s):// prefix')
			countsBNS = 1
		if message.content.split()[1].startswith('!!') == False and countsBNS == 0:
			await client.send_message(message.channel, 'Your edited command must have !! infront')
			countsBNS = 1
		if len(str(message.content).split()) !=3 and countsBNS == 0:
			await client.send_message(message.channel, 'Can only edit a link with exactly 3 arguments')
			countsBNS = 1
		if countsBNS == 0:
			saveL = ''
			dnBuildsSave = message.content.replace('!editbnsbuild ', '')
			with open('BNSBuilds.txt','r') as bnsBuilds2:
				for line in bnsBuilds2:
					if message.content.split()[1] in line:
						if str(message.author.id) not in line:
							await client.send_message(message.channel, 'This is not your build so you cannot edit it.')
							countsBNS = 1
						elif str(message.author.id) in line:
							saveL = line.rsplit(' ', 1)[0] + ' ' + message.content.split()[-1]
			saveL += '\n'
			if countsBNS == 0:
				newLines = []
				with open('BNSBuilds.txt','r') as bnsBuilds2:
					for line in bnsBuilds2:
						if message.content.split()[1] not in line:
							newLines.append(line)
						else:
							newLines.append(saveL)
				with open('BNSBuilds.txt','w') as bnsBuilds2:
					for line in newLines:
						bnsBuilds2.write(line)
				await client.send_message(message.channel, 'build "'+message.content.split()[2]+'" has been edited! Use your command "'+message.content.split()[1]+'" to use it!')
		countsBNS = 0
	
	if message.content.startswith('!deletebnsbuild'):
		if message.content == ('!deletebnsbuild') or message.content == ('!deletebnsbuild '):
			await client.send_message(message.channel, 'Your build must contain the format !deletebnsbuild !!(name of command)')
			countsBNS = 1
		elif message.content.split()[1].startswith('!!') == False:
			await client.send_message(message.channel, 'Your command created command must have !! infront')
			countsBNS = 1
		elif len(str(message.content).split()) !=2:
			await client.send_message(message.channel, 'Can only delete a link with exactly 2 arguments')
			countsBNS = 1
		elif countsBNS == 0:
			dnBuildsSave = message.content.replace('!deletebnsbuild ', '')
			with open('BNSBuilds.txt','r') as bnsBuilds2:
				for line in bnsBuilds2:
					if message.content.split()[1] in line:
						if str(message.author.id) not in line:
							await client.send_message(message.channel, 'This is not your build so you cannot delete it.')
							countsBNS = 1
			if countsBNS == 0:
				newLines = []
				with open('BNSBuilds.txt','r') as bnsBuilds2:
					for line in bnsBuilds2:
						if message.content.split()[1] not in line:
							newLines.append(line)
				with open('BNSBuilds.txt','w') as bnsBuilds2:
					for line in newLines:
						bnsBuilds2.write(line)
				await client.send_message(message.channel, 'Your build ' + message.content.split()[-1] + ' has been deleted.')
		countsBNS = 0
	if message.content.lower().startswith('!played'):
		g = {}
		with open("played.json") as j:
			g = json.load(j)
		sendout = "From what I know you\'ve played:\n``` "
		if message.author.id in g:
			for i in g[message.author.id].keys():
				if i != 'None':
					sSeconds = g[message.author.id][i][1]
					print(sSeconds)
					m, s = divmod(sSeconds, 60)
					h, m = divmod(m, 60)
					theTime = ("%d:%02d:%02d" % (h, m, s))
					sendout += (i + ': ' + str(theTime) + '\n')
		sendout += '```'
		await client.send_message(message.channel, sendout)

	# DN related ! commands to make the discord more integrated with dn
	#!pugs,trade,and mention will be put into 1 function since theyre practically the same thing, just different names and file names

	if message.content.lower().startswith('!dnpoints'):
		g = {}
		with open("played.json") as j:
			g = json.load(j)
		if message.author.id in g:
			if "Dragon Nest" in g[message.author.id]:
				sSeconds = g[message.author.id]["Dragon Nest"][1]
				dP = sSeconds/720
				await client.send_message(message.channel, "You have {} DN points!".format(dP))
			else:
				await client.send_message(message.channel, "I have not seen you play DN yet! go play!")
		else:
			await client.send_message(message.channel, "I have not seen you play DN yet! go play!")


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
				await client.send_message(message.channel, pugM + '\n\n' + i)
	elif message.content.startswith('!pugs') and str(message.channel.id) != '106300530548039680' and str(message.channel.server.id) == '106293726271246336':
		await client.send_message(message.channel, 'You can only call for pugs in the <#106300530548039680> channel.')
	elif message.content.startswith('!pugs') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
		await client.send_message(message.channel, 'You must have a topic to tell the people about what you are recruiting them for. It is BANNABLE if you do not have a legitamate topic on purpose.')
	elif message.content.lower().startswith('!pug') and str(message.channel.server.id) == '106293726271246336':
		pugL = ''
		with open('puglist.txt','r') as s:
			pugL = s.read()
		if message.author.mention not in pugL:
			with open('puglist.txt','a') as s:
				s.write(message.author.mention)
				s.write('\n')
				await client.send_message(message.channel, 'You have successfully signed up for pug mentions.')
		if message.author.mention in pugL:
			newL = []
			with open('puglist.txt','r') as s:
				for line in s:
					if message.author.mention not in line:
						newL.append(line)
			with open('puglist.txt','w') as s:
				for line in newL:    
					s.write(line)
			await client.send_message(message.channel, 'You have successfully removed yourself for pug mentions.')
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
				await client.send_message(message.channel, tradeM + '\n\n' + i)
	elif message.content.startswith('!trades') and str(message.channel.id) != '106301265817931776' and str(message.channel.server.id) == '106293726271246336':
		await client.send_message(message.channel, 'You can only call for trades in the <#106301265817931776> channel.')
	elif message.content.startswith('!trades') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
		await client.send_message(message.channel, 'You must have a topic to tell the people about what you want to trade. It is BANNABLE if you do not have a legitamate topic on purpose.')
	elif message.content.lower().startswith('!trade') and str(message.channel.server.id) == '106293726271246336':
		tradeL = ''
		with open('tradelist.txt','r') as s:
			tradeL = s.read()
		if message.author.mention not in tradeL:
			with open('tradelist.txt','a') as s:
				s.write(message.author.mention)
				s.write('\n')
				await client.send_message(message.channel, 'You have successfully signed up for trade mentions.')
		if message.author.mention in tradeL:
			newL = []
			with open('tradelist.txt','r') as s:
				for line in s:
					if message.author.mention not in line:
						newL.append(line)
			with open('tradelist.txt','w') as s:
				for line in newL:    
					s.write(line)
			await client.send_message(message.channel, 'You have successfully removed yourself for trade mentions.')
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
				await client.send_message(message.channel, pvpM + '\n\n' + i)
	elif message.content.startswith('!pvping') and str(message.channel.id) != '106300621459628032' and str(message.channel.server.id) == '106293726271246336':
		await client.send_message(message.channel, 'You can only call for pvp in the <#106300621459628032> channel.')
	elif message.content.startswith('!pvping') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
		await client.send_message(message.channel, 'You must have a topic to tell the people about your pvp request. It is BANNABLE if you do not have a legitamate topic on purpose.')
	elif message.content.lower().startswith('!pvp') and str(message.channel.server.id) == '106293726271246336':
		pvpL = ''
		with open('pvplist.txt','r') as s:
			pvpL = s.read()
		if message.author.mention not in pvpL:
			with open('pvplist.txt','a') as s:
				s.write(message.author.mention)
				s.write('\n')
				await client.send_message(message.channel, 'You have successfully signed up for pvp mentions.')
		if message.author.mention in pvpL:
			newL = []
			with open('pvplist.txt','r') as s:
				for line in s:
					if message.author.mention not in line:
						newL.append(line)
			with open('pvplist.txt','w') as s:
				for line in newL:    
					s.write(line)
			await client.send_message(message.channel, 'You have successfully removed yourself for pvp mentions.')

	elif message.content.startswith('!savednbuild'):
		print(message.content.split()[-1])
		print(message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com'))
		countsBNS = 0
		if message.content == ('!savednbuild') or message.content == ('!savednbuild ') and countsBNS == 0:
			await client.send_message(message.channel, 'Your build must contain the format !savednbuild $(name of command) (tree build url)')
			countsBNS = 1
		if message.content.split()[-1].startswith('https://dnss.herokuapp.com') == False and countsBNS == 0:
			if message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') == False and countsBNS == 0:
				if message.content.split()[-1].startswith('https://dnmaze.com') == False and countsBNS == 0:
					await client.send_message(message.channel, 'Your URL must be from dnss.herokuapp.com, dnss-kr.herokuapp.com or https://dnmaze.com or is missing the https:// prefix')
					countsBNS = 1
		print(message.content.split()[1].startswith('$'))
		print(message.content.split()[1])
		if message.content.split()[1].startswith('$') == False and countsBNS == 0:
			await client.send_message(message.channel, 'Your command created command must have $ infront')
			countsBNS = 1
		if len(str(message.content).split()) !=3 and countsBNS == 0:
			await client.send_message(message.channel, 'Can only create a link with exactly 3 arguments')
			countsBNS = 1
		if len(message.content.split()) == 3 and '$' in message.content.split()[1] and countsBNS == 0: 
			with open('DNbuilds.txt','r+') as dnBuilds:
				for line in dnBuilds:
					if message.content.split()[1] in line:
						await client.send_message(message.channel, 'A build with this name already exists!')
						countsBNS = 1
		if countsBNS == 0:
			dnBuildsSave = message.content.replace('!savednbuild ', '')
			with open('DNbuilds.txt','a') as bnsBuilds2:
				bnsBuilds2.write(str(message.author.id) + ' ' + dnBuildsSave + '\n')
				await client.send_message(message.channel, 'build "'+message.content.split()[2]+'" saved! Use your command "'+message.content.split()[1]+'" to use it!')
		countsBNS = 0
		pmCount = 1
	elif message.content.startswith('$') and counts1 == 0:
		with open('DNbuilds.txt') as readBuilds:
			for line in readBuilds:
				if message.content.split()[0] == line.split()[-2]:
					await client.send_message(message.channel, line.split()[-1])
					counts1 = 1
		counts1 = 0
		pmCount = 1
	elif message.content.startswith('!mydnbuilds'):
		tempCount = 1
		with open('DNbuilds.txt') as readBuilds:
			for line in readBuilds:
				if str(message.author.id) in line or str(message.author) in line:
					await client.send_message(message.channel, str(tempCount)+': '+line.replace(str(message.author.id)+ ' ', ''))
					tempCount += 1
		if tempCount == 1:
			await client.send_message(message.channel, 'You have no saved builds!')
		pmCount = 1
	elif message.content.startswith('!editdnbuild'):
		countsBNS = 0
		if message.content == ('!editdnbuild') or message.content == ('!editdnbuild ') and countsBNS == 0:
			await client.send_message(message.channel, 'Your build must contain the format !editdnbuild $(name of command) (tree build url)')
			countsBNS = 1
		if message.content.split()[-1].startswith('https://dnss.herokuapp.com') == False and countsBNS == 0:
			if message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') == False and countsBNS == 0:
				if message.content.split()[-1].startswith('https://dnmaze.com') == False and countsBNS == 0:
					await client.send_message(message.channel, 'Your URL must be from dnss.herokuapp.com ,dnss-kr.herokuapp.com or http://dnmaze.com/ or is missing the http(s):// prefix')
					countsBNS = 1
		if len(message.content.split()) == 2 and message.content.split()[1].startswith('$') == False and countsBNS == 0:
			await client.send_message(message.channel, 'Your edited command must have $ infront')
			countsBNS = 1
		if len(str(message.content).split()) !=3 and countsBNS == 0:
			await client.send_message(message.channel, 'Can only edit a link with exactly 3 arguments')
			countsBNS = 1
		if countsBNS == 0:
			saveL = ''
			dnBuildsSave = message.content.replace('!editdnbuild ', '')
			with open('DNbuilds.txt','r') as bnsBuilds2:
				for line in bnsBuilds2:
					if message.content.split()[1] in line:
						if str(message.author.id) not in line:
							await client.send_message(message.channel, 'This is not your build so you cannot edit it.')
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
				await client.send_message(message.channel, 'build "'+message.content.split()[2]+'" has been edited! Use your command "'+message.content.split()[1]+'" to use it!')
		countsBNS = 0
		pmCount = 1
	
	elif message.content.startswith('!deletednbuild'):
		countsBNS = 0
		if message.content == ('!deletednbuild') or message.content == ('!deletednbuild ') and countsBNS == 0:
			await client.send_message(message.channel, 'Your build must contain the format !deletednbuild $(name of command)')
			countsBNS = 1
		if len(message.content.split()) == 2 and message.content.split()[1].startswith('$') == False and countsBNS == 0:
			await client.send_message(message.channel, 'Your command created command must have $ infront')
			countsBNS = 1
		if len(str(message.content).split()) !=2 and countsBNS == 0:
			await client.send_message(message.channel, 'Can only delete a link with exactly 2 arguments')
			countsBNS = 1
		if countsBNS == 0:
			dnBuildsSave = message.content.replace('!deletednbuild ', '')
			with open('DNbuilds.txt','r') as bnsBuilds2:
				for line in bnsBuilds2:
					if message.content.split()[1] in line:
						if str(message.author.id) not in line:
							await client.send_message(message.channel, 'This is not your build so you cannot delete it.')
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
				await client.send_message(message.channel, 'Your build ' + message.content.split()[-1] + ' has been deleted.')

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
			await client.send_message(message.channel, 'Would you like me to PM you a list of community saved builds for {}?'.format(requestedBuilds))
			resp = await client.wait_for_message(author=message.author)
			if 'y' not in resp.content.lower():
				await client.send_message(message.channel, 'ok')
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
					await client.send_message(message.channel, 'I\'m sorry, there appears to be no build for the class(es) requested :(')
				else:
					if noB == True:
						await client.send_message(message.channel, 'I\'m sorry, there appears to be no build(s) made for one or more of the classes you requested :(')
					await client.send_message(message.channel, 'I will send you the PM now!')
					for i in pmlist:
						await client.send_message(message.author, i)
	if message.channel.id == '106301265817931776' and (message.content.lower().startswith("s") or message.content.lower().startswith("b")):
		trades = {}
		item = ''
		found = False
		with open("trading.json") as j:
			trades = json.load(j)
		for category in trades["rubric"]:
			for name in trades["rubric"][category]:
				if name in message.content.lower():
					item = category
					found = True
					break
			if found == True:
				break
		for category in trades["selling"]:
			tempchk = False
			for i in trades["selling"][category]:
				if len(trades["selling"][category][i]) != 0:
					for j in trades["selling"][category][i].keys():
						d = datetime.strptime(trades["selling"][category][i][str(j)]["datetime"], "%Y-%m-%d %H:%M:%S.%f")
						diff = d - datetime.now()
						if diff.days < 0:
							trades["selling"][category][i].pop(str(j))
							if len(trades["selling"][category][i]) == 0:
								trades["selling"][category].pop(i)
							with open('trading.json', 'w') as f:
								json.dump(trades, f, indent = 4)
							break
		if message.content.lower().startswith('search market'):
			await client.send_message(message.channel, "From what categories would you like to search? Only one category at a time. **All items in discord market are items registered by other users**")
			cata = []
			for i in trades["selling"]:
				cata.append(i)
			await client.send_message(message.channel, cata)
			resp = await client.wait_for_message(timeout = 60, author=message.author)
			if resp is None:
				return
			else:
				if resp.content.lower() in cata:
					if len(trades["selling"][resp.content.lower()]) == 0:
						await client.send_message(message.channel, "Sorry, there appears to be nothing listed :(")
					else:
						await client.send_message(message.channel, "I am sending you the PM")
						for i in trades["selling"][resp.content.lower()]:
							for j in trades["selling"][resp.content.lower()][i]:
								p = discord.utils.get(message.server.members, id = i).name
								newitem = trades["selling"][resp.content.lower()][i][str(j)]["description"]
								diff = datetime.strptime(trades["selling"][resp.content.lower()][i][str(j)]["datetime"], "%Y-%m-%d %H:%M:%S.%f") - datetime.now()
								dura = diff.days
								await client.send_message(resp.author, "Owner: {},\n**__Description:__** {}. time remaining: {} day(s)".format(p,newitem,dura))

				else:
					await client.send_message(message.channel, "Sorry, what you wrote was not one of the categories i listed out :(")
		elif message.content.lower().startswith('s>'):
			await client.send_message(message.channel, message.author.mention+", Since you seem to be selling something, would you like me to register your item in the DN discord marketplace so people can see it? type yes or no so i can know!")
			if len(item) == 0:
				await client.send_message(message.channel, "Because i could not match a category to what you are selling, the item will be placed in the 'other' category.")
				item = 'other'
			resp = await client.wait_for_message(timeout = 60, author=message.author)
			if 'no' in resp.content.lower():
				return
			else:
				r = resp.content.lower().split()
				await client.send_message(message.channel, 'OK! __Just follow these steps!:__\n**1.Give me a description of the item you\'re selling.** Can be an image, forum link to your post, etc.\n\n**2.Then tell me how many days you want this to be registered for at the __end of your description__**, please give me a numercal value before the word \'day(s)\' or this wont work. The max amount of days an item can be registered for is 30\n\n **Example**\ni want to sell a brutal plate, so i would tell it:\n"selling brutal plate c/o: 2k, b/o 4k x days", where \'x\' is the amount of days you want it in there.')
				resp = await client.wait_for_message(timeout = 300, author=message.author)
				if resp is None:
					return
				elif 'day' not in resp.content.lower():
					await client.send_message(message.channel, "sorry, you need to tell me how many days you want to have this up in the database.")
					return
				else:
					r = resp.content.lower().split()
					theword = ''
					if 'day' in r:
						if type(int(r[r.index('day') - 1])) != type(1):
							await client.send_message(message.channel, "invalid number before 'day'")
							return
						else:
							theword = 'day'
					if 'days' in r:
						if type(int(r[r.index('days') - 1])) != type(1):
							await client.send_message(message.channel, "invalid number before 'days'")
							return
						else:
							theword = 'days'
					if int(r[r.index(theword) - 1]) > 30:
						await client.send_message(message.channel, "you cannot set an end time that is greater than 30 days")
						return
					thenum = 0
					try:
						if len(trades["selling"][item][resp.author.id]) > 0:
							thenum = len(trades["selling"][item][resp.author.id])
							print(thenum)
							if len(trades["selling"][item][resp.author.id][str(thenum)]) > 0:
								print("test")
								for i in range(len(trades["selling"][item][resp.author.id])):
									trades["selling"][item][resp.author.id][str(i)] = trades["selling"][item][resp.author.id].pop(list(trades["selling"][item][resp.author.id].keys())[i])
									print("another test")
					except:
						pass

					a = {"description":resp.content,"datetime":str(datetime.now()+timedelta(days =int(r[r.index(theword) - 1])))}
					try:
						trades["selling"][item][resp.author.id][str(thenum)] = a
					except KeyError:
						newA = {resp.author.id:{str(thenum):{"description":resp.content,"datetime":str(datetime.now()+timedelta(days =int(r[r.index(theword) - 1])))}}}
						trades["selling"][item].update(newA)
					with open('trading.json', 'w') as f:
						json.dump(trades, f, indent = 4)
					await client.send_message(message.channel, "Your item has been registered with your description, and is under the '{}' category for {} day(s)".format(item,r[r.index(theword) - 1]))
		elif message.content.lower().startswith('b>'):
			if len(item) == 0:
				item = 'other'
			await client.send_message(message.channel, '{}, Would you like me to PM you all items that are currently being sold under \'{}\'? type yes or no so i can know.'.format(message.author.mention,item))
			resp = await client.wait_for_message(timeout = 60, author=message.author)
			if resp is None:
				return
			elif 'no' in resp.content.lower():
				await client.send_message(message.channel, 'ok')
				return
			else:
				if len(trades["selling"][item]) == 0:
					await client.send_message(message.channel, "Sorry, there appears to be nothing listed :(")
				else:
					await client.send_message(message.channel, "I am sending you the PM")
					for i in trades["selling"][item]:
						for j in range(len(trades["selling"][item][i])):
							p = discord.utils.get(message.server.members, id = i).name
							newitem = trades["selling"][item][i][str(j)]["description"]
							diff = datetime.strptime(trades["selling"][item][i][str(j)]["datetime"], "%Y-%m-%d %H:%M:%S.%f") - datetime.now()
							dura = diff.days
							await client.send_message(resp.author, "Owner: {},\n**__Description:__** {}. time remaining: {} day(s)".format(p,newitem,dura))




# other commands
	if message.channel.server.id == '109902387363217408':
		if message.content.lower().startswith('!cats'):
			rcats = random.choice(os.listdir("C:/DISCORD BOT/cats"))
			await client.send_file(message.channel, 'C:/DISCORD BOT/cats/'+rcats)

	if message.author.id == '90886475373109248':
		if message.content.startswith('!join') and len(message.content.split()) == 2:
			try:
				await client.accept_invite(message.content.split()[1])
				await client.send_message(message.channel, 'Joined successfully!')
			except:
				await client.send_message(message.channel, 'didnt work :(')
		if message.content.startswith('!debug'):
			deb = message.content[7:]
			await client.send_message(message.channel, str(eval(deb)))
	if message.content.startswith('<@106469383206883328>'):
		if 'who are you' == str(message.content).lower().replace('<@106469383206883328>'+ ' ', '') or 'who are you?' == str(message.content).lower().replace('<@106469383206883328>'+ ' ', ''):
			await client.send_message(message.channel, 'I am a bot that runs on a community made python API(more info on that in bot-and-api channel) and programmed by Comphus to have functions for this discord server')
			counts1 = 1
		elif counts1 == 0:
			for word in qQuestion:
				if word in str(message.content).lower():
					await client.send_message(message.channel, magicEight[random.randint(0,19)]+', ' +  message.author.mention)
					counts1 = 1
					break  
		if counts1 == 1:
			counts1 = 0
		elif 'hi' in message.content or 'Hi' in message.content or 'hello' in message.content or 'Hello' in message.content:
			await client.send_message(message.channel, 'Hi! ' + message.author.mention)
		elif 'bye' in message.content or 'Bye' in message.content:
			await client.send_message(message.channel, 'Bye-Bye! ' + message.author.mention)
		elif 'i love you' in message.content or 'I love you' in message.content or '<3' in message.content:
			await client.send_message(message.channel, 'I love you too <3 ' + message.author.mention)
		elif 'thank' in message.content or 'Thanks' in message.content:
			await client.send_message(message.channel, 'You\'re welcome! ' + message.author.mention)
		elif 'fuck you' in message.content or 'Fuck you' in message.content or 'Fuck u' in message.content or 'fuck u' in message.content or '( ° ͜ʖ͡°)╭∩╮' in message.content:
			await client.send_message(message.channel, '( ° ͜ʖ͡°)╭∩╮ ' + message.author.mention)
		else:
			await client.send_message(message.channel, 'what? ' + message.author.mention)

	if message.content.startswith('!giveaway') and message.author.id == '90886475373109248':
		r = random.randint(0,len(message.server.members)-1)
		winner = message.server.members[r]
		#print(winner)
		await client.send_message(message.channel, '<@90844964413505536>		')
		person = await client.wait_for_message(timeout = 60, author = winner)
		if person is None:
			await client.send_message(message.channel, "sorry you took too long, please roll again!")
		elif len(person.content) > 0:
			await client.send_message(message.channel, "Congratulations {}, You've won!".format(winner.mention))
			print('they won')






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


