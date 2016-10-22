import discord
import asyncio
from datetime import datetime, date, timedelta
import json
import re
import fileinput
import io
import os
from math import *
import time
import random
import logging
import codecs
import shelve

from BASEDBOTgames import *
from BASEDBOTbns import *
from BASEDBOTow import *
from BASEDBOTdn import *
from BASEDBOTetc import *
from BASEDBOTmusic import *

if not discord.opus.is_loaded():
	discord.opus.load_opus('opus')
logging.basicConfig()
client = discord.Client()


tPlayers = {}
tt = False
tStop = 0
QuizResponses = {}
with open("triviacontent.json") as j:
	QuizResponses = json.load(j)
blacklist = ['128044950024617984']
karaokelist = []
spotlight = False
slowM = False
slowT = 0
with open('bnsemotes.txt') as inputF:
	bnsEmotes = inputF.read().splitlines()
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



@client.async_event
def on_member_join(member):
	if member.server.id not in '82210263440306176 110373943822540800':
		try:
			if str(member.server.id) not in '106293726271246336 148358898024316928':
				yield from client.send_message(member.server, 'Welcome ' + member.mention + ' to the server!')
		except:
			pass
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


@client.event
async def on_message(message):
	global slowM
	global slowT
	global karaokelist
	global spotlight
	global tStop
	global tt
	global tPlayers
	cTime = datetime.now()

	if client.user == message.author:
		return
	if message.channel.id == '168949939118800896':
		return
	if message.author.id in blacklist:
		return
	
	if message.content.startswith('!removeallmsgs') and message.author.id == '90886475373109248':
		logs =  client.logs_from(message.channel)
		async for log in logs:
			await client.delete_message(log)

	if message.content.startswith('!delete ian'):
		with codecs.open('daddy.txt','r',"utf-8") as f:
			for i in f:
				await client.send_message(message.channel, i)
				await asyncio.sleep(2)
	if message.content.startswith('!yesh') and message.server.id == '90944254297268224':
		await client.send_message(message.channel, """<:Heck1:235258589621649408><:Heck2:235258604448382978><:Fucking:235256098427240451>\n<:Heck4:235258621955407872><:Man:235256139514773504><:Im:235256149455273984>\n<:Fuckin:235256165804539906><:Cumming:235256179045957633><:Cx:235256191154913280>""")
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
	
	if message.content.startswith('!vanish') and len(message.content.split()) == 3 and (message.author.id in dMods or message.author.id in '105130465039548416' or message.author.server_permissions.administrator) and type(1) == type(int(message.content.split()[2])) and len(message.mentions) > 0:
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

	if message.content.startswith('!') and message.content.lower().split()[0] in MainResponses['all!commands']:
		if message.content.lower().startswith("!commands"):
			await client.send_message(message.author, MainResponses['all!commands'][message.content.lower().split()[0]])
		else:
			await client.send_message(message.channel, MainResponses['all!commands'][message.content.lower().split()[0]])
		return
	if '!' in message.content and message.server.id not in '119222314964353025':
		for i in message.content.lower().split():
			if i.startswith('!'):
				if i.replace('!','') in bnsEmotes:
					await client.send_file(message.channel, 'C:/DISCORD BOT/bns emotes/'+i.replace('!','')+'.png')
					return
		
	if message.content in unicodeResponses:
		await client.send_message(message.channel, unicodeResponses[message.content.lower().split()[0]])
	elif message.content.startswith('!hello'):
		await client.send_message(message.channel, 'hi')
	elif message.content.startswith('!c4'):
		c4 = {}
		with open("connect4.json") as j:
			c4 = json.load(j)
		if message.author.id in c4.keys():
			pass
		results = connect4(message)
		await client.send_message(message.channel, results)
	elif message.content.startswith('!duel') and str(message.channel.id) not in '91518345953689600 106293726271246336':    
		results = dueling([message.mentions[0],message.mentions[1]])
		await client.send_message(message.channel, results[1])
		for i in range(len(results[0])):
			dDelay = random.randint(3,5)
			await client.send_message(message.channel, results[0][i])
			await asyncio.sleep(dDelay)
		await client.send_message(message.channel, results[2])
	elif message.content.lower().startswith('!rps') and len(message.mentions) == 2:
		players = [message.mentions[0].mention,message.mentions[1].mention]
		results = await rpc(players)
		async def rpcresults(r):
			players = [message.mentions[0].mention,message.mentions[1].mention]
			if r[1] == 0:
				await client.send_message(message.channel, r[0])
				await client.send_message(message.channel, "It looks like you two have tied! Would you like to try again {}? Type **yes** or **no**".format(message.author.mention))
				resp = await client.wait_for_message(timeout = 60, author=message.author)
				if resp is None:
					return
				if 'n' in resp.content.lower():
					return
				elif 'y' in resp.content.lower():
					res = await rpc(players)
					await rpcresults(res)
					return
			elif r[1] == 1:
				await client.send_message(message.channel, r[0])
				return
			elif r[1] == 2:
				await client.send_file(message.channel, 'C:/Users/gabriel/Pictures/BnS/donkay.png')
				await client.send_message(message.channel, "You have been visited by the __Mystical__ **DonkaDonks**, you both _Lose_!")
				return
		await rpcresults(results)
	elif message.content.lower().startswith('!rps') and len(message.mentions) != 2:
		await client.send_message(message.channel, "You must mention two people in order to play.")
	elif message.content.startswith('|trivia') and tt == False and message.channel.id != '106293726271246336':
		tPlayers = {}
		tt == True
		tStop = 1
		await client.send_message(message.channel, "You have started the Overwatch Trivia! These questions will start up in 5 seconds! Use |stop to stop the trivia and |points to see points!")
		TriviaQuestions = QuizResponses['overwatch']
		print(len(TriviaQuestions))
		await asyncio.sleep(2)
		while len(TriviaQuestions) > 0 and tStop == 1:
			await asyncio.sleep(3)
			TriviaQuestion = random.choice(list(TriviaQuestions.keys()))
			await client.send_message(message.channel, "**The question is:**\n{}".format(TriviaQuestion))
			answer = TriviaQuestions[TriviaQuestion]
			end_time = time.time() + 15
			while True:
				time_remaining = end_time - time.time()
				if time_remaining <= 0:
					await client.send_message(message.channel, '**Sorry, you took too long! The answer was:**\n```xl\n{}```'.format(answer))
					del TriviaQuestions[TriviaQuestion]
					break
				guess = await client.wait_for_message(timeout = time_remaining)
				if guess and answer in guess.content.lower():
					await client.send_message(message.channel, '**Congratulations** {}! **You\'ve won!**'.format(guess.author.mention))
					if guess.author.mention not in tPlayers:
						tPlayers[guess.author.mention] = 1
					elif guess.author.mention in tPlayers:
						tPlayers[guess.author.mention] += 1
					del TriviaQuestions[TriviaQuestion]
					break
			print(len(TriviaQuestions))
		if len(TriviaQuestions) == 0 and message.channel.id != '106293726271246336':
			await client.send_message(message.channel, "There are no more questions left!")
			tt = False
			tStop = 0
			a = '**RESULTS**\n'
			for i in tPlayers:
				a+= '{} with {} points\n'.format(i,tPlayers[i])
			await client.send_message(message.channel, a)
			tPlayers = {}
			return
	elif message.content.startswith('|stop') and message.channel.id != '106293726271246336':
		print('hi')
		if tStop != 1:
			await client.send_message(message.channel, 'Trivia hasnt started yet!')
			return
		if tStop == 1:
			await client.send_message(message.channel, "Trivia has stopped! The last question will continue!")
			tt == False
			tStop = 0
			a = '**RESULTS**\n'
			for i in tPlayers:
				a+= "{} with {} points\n".format(i,tPlayers[i])
			await client.send_message(message.channel, a)
			tPlayers = {}
		print('hello')
		return
	elif message.content.startswith('|points') and message.channel.id != '106293726271246336':
		a = '**RESULTS**\n'
		for i in tPlayers:
			a+= '{} with {} points\n'.format(i,tPlayers[i])
		await client.send_message(message.channel, a)
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
	if message.content.startswith("!yt"):
		startmusic = musicbot(client)
		await startmusic.playmusic(message, message.server.id)
	if message.channel.is_private == False and message.channel.server.id == '106293726271246336':
		with io.open('chatLogs.txt','a',encoding='utf-8') as f:
			logT = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
			logM = (str(message.author)+'('+str(message.author.id)+') '+ logT +': '+str(message.content)+'\n')
			f.write(logM)
		if message.content.startswith('!chatlogs') and message.author.id in dAdmins and message.channel.id == '106301620500836352':
			await client.send_file(message.channel, 'chatLogs.txt')
		if message.content.startswith("!evlogs") and message.author.id in dAdmins and message.channel.id == '106301620500836352':
			await client.send_file(message.channel, 'eventlist.txt')
		if any(reg.lower() in message.content.lower() for reg in MainResponses["regions"]) and message.content.startswith('!'):
			for i in MainResponses["regions"]:
				for j in message.author.roles:
					if i in j.name and i.lower() == message.content.lower().replace('!', ''):
						await client.remove_roles(message.author, discord.utils.get(message.server.roles, name = i))
						await asyncio.sleep(1)
						return
				if i.lower() == message.content.lower().replace('!', ''):
					await client.add_roles(message.author, discord.utils.get(message.server.roles, name = i))
					await asyncio.sleep(1)
					return

			"""
		if message.content.startswith("!raisehand"):
			mrole = discord.utils.get(message.server.roles, name = 'hand raised')
			srole = discord.utils.get(message.server.roles, name = 'spotlight')
			rlist = []
			for i in message.author.roles:
				rlist.append(i.name)
			if 'hand raised' not in rlist:
				await client.add_roles(message.author, mrole)
				await client.send_message(message.channel, 'You have raised your hand!')
				karaokelist.append(message.author)
				if len(karaokelist) == 1:
					spotlight = message.author
					await client.add_roles(message.author, srole)
			elif 'hand raised' in rlist:
				await client.remove_roles(message.author, mrole)
				await client.send_message(message.channel, 'You have put down your hand!')
				karaokelist.remove(message.author)

		if message.content.startswith('!klist'):
			s = '```'
			for i in range(len(karaokelist)):
				s += str(i) + '. ' + karaokelist[i].name + '\n'
			s += '```'
			await client.send_message(message.channel, s)
		if message.content.startswith('!kskip') and message.author.id in dMods:
			mrole = discord.utils.get(message.server.roles, name = 'hand raised')
			srole = discord.utils.get(message.server.roles, name = 'spotlight')
			await client.remove_roles(karaokelist[0], mrole)
			await asyncio.sleep(1)
			await client.remove_roles(karaokelist[0], srole)
			karaokelist.pop(0)
			if len(karaokelist) > 0:
				spotlight = karaokelist[0]
				await client.add_roles(spotlight, srole)
			"""
			




	if message.content.startswith('!define') and message.channel.id != '106293726271246336':
		await client.send_message(message.channel, defines(message))
	if message.content.startswith('!checktwitch'):
		await client.send_message(message.channel, checktwitch(message))
	if message.content.lower().startswith('!mal') and message.channel.id not in '106293726271246336':
		await client.send_message(message.channel, mal(message))
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

	if message.content.startswith('!shoot') and len(message.content.split()) == 2:
		shoot = shooting(client)
		await shoot.shoots(message, message.channel)
	if message.content.startswith('!gimmepoutine'):
		await client.send_file(message.channel, 'poutine.jpg')

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
		elif message.channel.is_private == False:
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
		dCol1 = p.colour
		dJoin = p.joined_at
		for i in p.roles:
			dRol += i.name + ', '
			if i.position > dCol:
				dCol1 = i
				dCol = i.position
		dCol2 = hex(dCol1.value)
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
	if message.content.startswith('!chid'):
		await client.send_message(message.channel, message.channel.id)
	if message.content.startswith('!serverid'):
		await client.send_message(message.channel, message.channel.server.id)

	#the one overwatch command
	if len(message.content.split()) > 1 and message.content.lower().split()[0] == '!ow' and message.channel.id != '106293726271246336':
		await client.send_message(message.channel, ow(message.content[4:]))
		return

	#BNS commands
	if message.content.startswith('!bnstree'):
		await client.send_message(message.channel, bnstree(message))
		return
	if message.content.lower().startswith('!bns') and message.channel.id != '106293726271246336 88422130479276032 124934505810100224 146298657765851137 144803652635328512':
		await client.send_message(message.channel, bns(message))
	if message.content.startswith('!savebnsbuild'):
		await client.send_message(message.channel, savebnsbuild(message))
	if message.content.startswith('!editbnsbuild'):
		await client.send_message(message.channel, editbnsbuild(message))
	if message.content.startswith('!deletebnsbuild'):
		await client.send_message(message.channel, deletebnsbuild(message))
	if message.content.startswith('!mybnsbuilds'):
		for line in mybnsbuilds(message):
			await client.send_message(message.channel, line)
	if message.content.startswith('!!'):
		if prefixbnscommands(message) == None:
			return
		else:
			await client.send_message(message.channel, prefixbnscommands(message))
	"""
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
	"""

	# DN related ! commands to make the discord more integrated with dn
	#!pugs,trade,and mention will be put into 1 function since theyre practically the same thing, just different names and file names
	"""
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
	"""

	if message.content.lower().startswith('!pug') and str(message.channel.id) != '106293726271246336' and message.channel.server.id == '106293726271246336':
		mrole = discord.utils.get(message.server.roles, name = 'pug')
		rlist = []
		for i in message.author.roles:
			rlist.append(i.name)
		if 'pug' not in rlist:
			await client.add_roles(message.author, mrole)
			await client.send_message(message.channel, 'You have signed up for <#106300530548039680> mentions!')
		elif 'pug' in rlist:
			await client.remove_roles(message.author, mrole)
			await client.send_message(message.channel, 'You have removed yourself from <#106300530548039680> mentions!')
	elif message.content.lower().startswith('!trade') and str(message.channel.id) != '106293726271246336':
		mrole = discord.utils.get(message.server.roles, name = 'trade')
		rlist = []
		for i in message.author.roles:
			rlist.append(i.name)
		if 'trade' not in rlist:
			await client.add_roles(message.author, mrole)
			await client.send_message(message.channel, 'You have signed up for <#106301265817931776> mentions!')
		elif 'trade' in rlist:
			await client.remove_roles(message.author, mrole)
			await client.send_message(message.channel, 'You have removed yourself from <#106301265817931776> mentions!')
	elif message.content.lower().startswith('!pvp') and str(message.channel.id) != '106293726271246336':
		mrole = discord.utils.get(message.server.roles, name = 'pvp')
		rlist = []
		for i in message.author.roles:
			rlist.append(i.name)
		if 'pvp' not in rlist:
			await client.add_roles(message.author, mrole)
			await client.send_message(message.channel, 'You have signed up for <#106300621459628032> mentions!')
		elif 'pvp' in rlist:
			await client.remove_roles(message.author, mrole)
			await client.send_message(message.channel, 'You have removed yourself from <#106300621459628032> mentions!')
	elif '@pug' in message.clean_content and message.channel.id != '106300530548039680':
		m = await client.send_message(message.channel, "{} You can only mention the trade role in the <#106300530548039680> channel. This message will be deleted in 15 seconds".format(message.author.mention))
		with io.open('attempts.txt','a',encoding='utf-8') as attempts:
			attempts.write('{}({}) attempted to mention @pug on {}UTC outside of the pug channel. They said: {}\n'.format(message.author.id, message.author.name, str(message.timestamp), message.content))
		await client.delete_message(message)
		await asyncio.sleep(15)
		await client.delete_message(m)
	elif '@trade' in message.clean_content and message.channel.id != '106301265817931776' and message.channel.server.id == '106293726271246336':
		m = await client.send_message(message.channel, "{} You can only mention the trade role in the <#106301265817931776> channel. This message will be deleted in 15 seconds".format(message.author.mention))
		with io.open('attempts.txt','a',encoding='utf-8') as attempts:
			attempts.write('{}({}) attempted to mention @trade on {}UTC outside of the trade channel. They said: {}\n'.format(message.author.id, message.author.name, str(message.timestamp), message.content))
		await client.delete_message(message)
		await asyncio.sleep(15)
		await client.delete_message(m)
	elif '@pvp' in message.clean_content and message.channel.id != '106300621459628032' and message.channel.server.id == '106293726271246336':
		m = await client.send_message(message.channel, "{} You can only mention the pvp role in the <#106300621459628032> channel. This message will be deleted in 15 seconds".format(message.author.mention))
		with io.open('attempts.txt','a',encoding='utf-8') as attempts:
			attempts.write('{}({}) attempted to mention @pvp on {}UTC outside of the pvp channel. They said: {}\n'.format(message.author.id, message.author.name, str(message.timestamp), message.content))
		await client.delete_message(message)
		await asyncio.sleep(15)
		await client.delete_message(m)

	elif message.content.lower().startswith('!skillbuilds') or message.content.lower().startswith('!krskillbuilds'):
		await client.send_message(message.channel, skillbuilds(message))
	elif message.content.startswith('!savednbuild'):
		await client.send_message(message.channel, savednbuild(message))
	elif message.content.startswith('!editdnbuild'):
		await client.send_message(message.channel, editdnbuild(message))
	elif message.content.startswith('!deletednbuild'):
		await client.send_message(message.channel, deletednbuild(message))
	elif message.content.startswith('!mydnbuilds'):
		for line in mydnbuilds(message):
			await client.send_message(message.channel, line)
	elif message.content.startswith('$') and len(message.content.split()) == 1:
		if prefixdncommands(message) == None:
			return
		else:
			await client.send_message(message.channel, prefixdncommands(message))
	elif message.channel.id == '107718615452618752': # skill-builds channel auto skill build distributor
		requestedBuild = []
		requestedBuilds = []
		m = message.content.lower()
		if 'build' in m and '?' in m and len(m.split()) > 1:
			m = m.replace('build', ' ')
			for i in MainResponses["t5dnskillbuilds"].values():
				if i in m:
					requestedBuild.append(i)
					m = m.replace(i, '')
			for i in MainResponses["t5dnskillbuilds"]:
				if i in m:
					requestedBuild.append(MainResponses["t5dnskillbuilds"][i])
					m = m.replace(MainResponses["t5dnskillbuilds"][i], '')
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
							if i in line.split()[-1]:
								try:
									pmlist.append(line.replace(line.split()[0], discord.utils.get(message.server.members, id = line.split()[0]).name))
									checksB += 1
								except:
									pmlist.append(line.replace(line.split()[0], 'Unknown User'))
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

# other commands
	if message.channel.is_private == False and message.channel.server.id == '109902387363217408':
		if message.content.lower().startswith('!cats'):
			rcats = random.choice(os.listdir("C:/DISCORD BOT/cats"))
			await client.send_file(message.channel, 'C:/DISCORD BOT/cats/'+rcats)

	if message.author.id == '90886475373109248':
		if message.content.startswith('!debug'):
			deb = message.content[7:]
			await client.send_message(message.channel, str(eval(deb)))
	if message.content.startswith('<@175433427175211008>'):
		if 'who are you' in message.content.lower():
			await client.send_message(message.channel, 'I am a bot that runs on a community made python API(more info on that in bot-and-api channel) and programmed by Comphus to have functions for the Dragon Nest NA Community Discord Server')
			return
		if any(word in message.content.lower() for word in MainResponses['qQuestion']):
			await client.send_message(message.channel, MainResponses['magicEight'][random.randint(0,19)]+', ' +  message.author.mention)
			return 
		elif 'hi' in message.content.lower() or 'hello' in message.content.lower():
			await client.send_message(message.channel, 'Hi! ' + message.author.mention)
		elif 'bye' in message.content.lower():
			await client.send_message(message.channel, 'Bye-Bye! ' + message.author.mention)
		elif 'i love you' in message.content.lower() or '<3' in message.content:
			await client.send_message(message.channel, 'I love you too <3 ' + message.author.mention)
		elif 'thank' in message.content.lower():
			await client.send_message(message.channel, 'You\'re welcome! ' + message.author.mention)
		elif 'fuck you' in message.content.lower() or 'fuck u' in message.content.lower() or '( ° ͜ʖ͡°)╭∩╮' in message.content:
			await client.send_message(message.channel, '( ° ͜ʖ͡°)╭∩╮ ' + message.author.mention)
		else:
			await client.send_message(message.channel, 'what? ' + message.author.mention)






@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	yield from client.change_presence(game=discord.Game(name='you like a fiddle'))

async def main_task():
	await client.login(dLogin['username'])
	await client.connect()

loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(main_task())
except Exception:
	loop.run_until_complete(client.close())
finally:
	loop.close()
