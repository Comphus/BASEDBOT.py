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
with open("triviacontent.json") as j:
	QuizResponses = json.load(j)
blacklist = ['128044950024617984']
karaokelist = []
spotlight = False
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


	if message.author.id == '90886475373109248':
		if message.content.startswith('!debug'):
			deb = message.content[7:]
			await client.send_message(message.channel, str(eval(deb)))
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


		
	if message.content in unicodeResponses:
		await client.send_message(message.channel, unicodeResponses[message.content.lower().split()[0]])
	elif message.content.startswith('!c4'):
		await games(client).c4(message)
	elif message.content.startswith('!duel') and str(message.channel.id) not in '91518345953689600 106293726271246336':    
		await games(client).duel(message)
	elif message.content.lower().startswith('!rps'):
		await games(client).rps(message)
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
		await games(client).dntrivia(message)
	if message.content.startswith("!yt"):
		await musicbot(client).playmusic(message, message.server.id)
	if message.channel.is_private == False and message.channel.server.id == '106293726271246336':
		with io.open('chatLogs.txt','a',encoding='utf-8') as f:
			logT = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
			logM = (str(message.author)+'('+str(message.author.id)+') '+ logT +': '+str(message.content)+'\n')
			f.write(logM)
		if any(reg.lower() in message.content.lower() for reg in MainResponses["regions"]) and message.content.startswith('!'):
			await botetc(client).regions(message)

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
			






	if message.content.startswith('!shoot') and len(message.content.split()) == 2:
		await shooting(client).shoots(message, message.channel)
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
	bns = bladeandsoul(client, message)
	if message.content.startswith('!bnstree'):
		await client.send_message(message.channel, bns.bnstree())
	elif message.content.lower().startswith('!bns') and message.channel.id != '106293726271246336 88422130479276032 124934505810100224 146298657765851137 144803652635328512':
		await client.send_message(message.channel, bns.bnssearch())
	elif message.content.startswith('!savebnsbuild'):
		await client.send_message(message.channel, bns.savebnsbuild())
	elif message.content.startswith('!editbnsbuild'):
		await client.send_message(message.channel, bns.editbnsbuild())
	elif message.content.startswith('!deletebnsbuild'):
		await client.send_message(message.channel, bns.deletebnsbuild())
	elif message.content.startswith('!mybnsbuilds'):
		await bns.mybnsbuilds()
	elif message.content.startswith('!!'):
		await bns.prefixbnscommands()

	#dn commands
	dn = dragonnest(client, message)
	if message.content.lower().startswith('!pug') and str(message.channel.id) != '106293726271246336' and message.channel.server.id == '106293726271246336':
		await dn.pug()
	elif message.content.lower().startswith('!trade') and str(message.channel.id) != '106293726271246336':
		await dn.trade()
	elif message.content.lower().startswith('!pvp') and str(message.channel.id) != '106293726271246336':
		await dn.pvp()
	elif '@pug' in message.clean_content and message.channel.id != '106300530548039680' and message.channel.server.id == '106293726271246336':
		await dn.pugmention()
	elif '@trade' in message.clean_content and message.channel.id != '106301265817931776' and message.channel.server.id == '106293726271246336':
		await dn.trademention()
	elif '@pvp' in message.clean_content and message.channel.id != '106300621459628032' and message.channel.server.id == '106293726271246336':
		await dn.pvpmention()
	elif message.content.lower().startswith('!skillbuilds') or message.content.lower().startswith('!krskillbuilds'):
		await client.send_message(message.channel, dn.skillbuilds())
	elif message.content.startswith('!savednbuild'):
		await client.send_message(message.channel, dn.savednbuild())
	elif message.content.startswith('!editdnbuild'):
		await client.send_message(message.channel, dn.editdnbuild())
	elif message.content.startswith('!deletednbuild'):
		await client.send_message(message.channel, dn.deletednbuild())
	elif message.content.startswith('!mydnbuilds'):
		await dn.mydnbuilds()
	elif message.content.startswith('$') and len(message.content.split()) == 1:
		await dn.customdncommands()
	elif message.channel.id == '107718615452618752': # skill-builds channel auto skill build distributor
		await dn.autobuilds()

# other commands
	if message.channel.is_private == False and message.channel.server.id == '109902387363217408':
		if message.content.lower().startswith('!cats'):
			rcats = random.choice(os.listdir("C:/DISCORD BOT/cats"))
			await client.send_file(message.channel, 'C:/DISCORD BOT/cats/'+rcats)
	if message.content.startswith('!') and message.content.lower().split()[0] in MainResponses['all!commands']:
		await botetc(client).mainprefixcommands(message)
	elif '!' in message.content and message.server.id not in '119222314964353025':
		await botetc(client).zealemotes(message)
	elif message.content.startswith('<@175433427175211008>'):
		await botetc(client).bbresponse(message)
	elif message.content.startswith('!define') and message.channel.id != '106293726271246336':
		await client.send_message(message.channel, defines(message))
	elif message.content.startswith('!checktwitch'):
		await client.send_message(message.channel, checktwitch(message))
	elif message.content.lower().startswith('!mal') and message.channel.id not in '106293726271246336':
		await client.send_message(message.channel, mal(message))
	elif message.content.startswith('!spookme'):
		await botetc(client).spookme(message)
	elif message.content.startswith('!delete ian'):
		await botetc(client).deleteian(message)
	elif message.content.startswith('!lightproc'):
		await botetc(client).lightproc(message)
	elif message.content.startswith('!yesh') and message.server.id == '90944254297268224':
		await client.send_message(message.channel, """<:Heck1:235258589621649408><:Heck2:235258604448382978><:Fucking:235256098427240451>\n<:Heck4:235258621955407872><:Man:235256139514773504><:Im:235256149455273984>\n<:Fuckin:235256165804539906><:Cumming:235256179045957633><:Cx:235256191154913280>""")







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
