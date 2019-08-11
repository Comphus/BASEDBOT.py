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
newcomes = {}
namecheck = {}
memrole = None
memtot = None
MainResponses = {}
BWSecurity = {}
counts1 = 0
countsBNS = 0

with open("MainResponses.json") as j:
	MainResponses = json.load(j)
with open("BWSecurity.json") as j:
	BWSecurity = json.load(j)
#welcomech = discord.utils.find(lambda r: r.name == 'Member', client.servers.roles)

@client.event
async def on_member_join(member):
	global newcomes
	global memrole
	global namecheck
	newcomes[member.id] = 0
	namecheck[member.id] = None
	memrole = member.server.roles
	memtot = member.server.members
	#print(memrole)
	passch = discord.utils.get(client.get_all_channels(), id ='148359551626772480')
	await asyncio.sleep(1)
	msg1 = await client.send_message(passch, 'Welcome ' + member.mention + '!')
	msg2 = await client.send_message(passch, "**Please PM me the password to this server**, you will be kicked in 10 minutes if I dont get a response. This message will be deleted in 2 minutes.")
	await asyncio.sleep(120)
	await client.delete_message(msg1)
	await client.delete_message(msg2)
	await asyncio.sleep(600)
	if newcomes[member.id] != 2:
		await client.send_message(member, "Sorry, you didnt give me the password in the alloted time or gave me an IGN, you will be kicked in 15 seconds")
		await asyncio.sleep(15)
		del newcomes[member.id]
		await client.kick(member)



@client.event
async def on_message(message):
	global newcomes
	global memrole
	global memtot
	global counts1
	global countsBNS
	global BWSecurity
	dt = datetime.now()
	allroles = list(client.servers)[0].roles
	for i in newcomes:
		try:
			if newcomes[i] == 2:
				await client.add_roles(discord.utils.get(message.server.members, id = i), discord.utils.find(lambda r: r.name == 'Members', memrole))
				del newcomes[i]
				print(newcomes)
				break
			break
		except:
			break
	if message.content.startswith('!removeallmsgs') and message.author.id == '90886475373109248':
		logs =  client.logs_from(message.channel)
		async for log in logs:
			await client.delete_message(log)
	if message.content.startswith('!vanish') and len(message.content.split()) == 3 and (message.author.id in '90886475373109248') and type(1) == type(int(message.content.split()[2])) and len(message.mentions) > 0:
		logs =  client.logs_from(message.channel)
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
	if message.content.startswith('!chid'):
		await client.send_message(message.channel, message.channel.id)
	if message.content.startswith('!serverid'):
		await client.send_message(message.channel, message.channel.server.id)
	if message.content.startswith('!changeme') and len(message.content.split()) >= 3 and (str(message.author.id) in '90886475373109248 90953831583617024 90869992689520640 90940396602953728 90847182772527104'):
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
	elif message.content.lower().split()[0] in MainResponses['all!commands']:
		await client.send_message(message.channel, MainResponses['all!commands'][message.content.lower().split()[0]])
		return


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
	if message.content.lower().startswith('!bns') and len(message.content.split()) > 1 and message.channel.id != '106293726271246336':
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
			#print(soup.find_all(attrs={"class":"signature"})[0].find_all("li")[1].find_all(attrs={"class":"masteryLv"})[0].string)#.find_all(attrs={"class":"desc"})[0])
			classname = soup.find_all(attrs={"class":"signature"})[0].find_all("ul")[0].li.string
			level = soup.find_all(attrs={"class":"signature"})[0].find_all("li")[1].text.split()[1]
			hmlevel = soup.find_all(attrs={"class":"signature"})[0].find_all("li")[1].find_all(attrs={"class":"masteryLv"})[0].string.replace("Dark Arts Levle", "**Dark Arts Levle:**")
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
			await client.send_message(message.channel, "**Class:** {}\n**Level:** {}\n{}\n**Attack:** {}                                                        **HP:** {}\n**Pierce:** {}({})                                          **Defense:** {}({})\n**Accuracy:** {}({})                                 **Evasion:** {}({})\n**Critical Hit:** {}({})                              **Block:** {}({})\n**Critical Damage** {}({})                    **Crit Defense:** {}({})".format(classname,level,hmlevel,att,hp,pierce,piercep,defense,defensep,acc,accp,eva,evap,chit,chitp,block,blockp,cdmg,cdmgp,critd,critdp))
			await client.send_message(message.channel, soup.find_all("div", class_="charaterView")[0].img['src'])
			return
		else:
			await client.send_message(message.channel, 'Character name does not exist')
			return
	if message.content.startswith('!bnsdaily'):
		await client.send_file(message.channel, "bnsdailymap.png")
		return
	if message.content.startswith('!bns') and len(message.content.split()) == 1:
		await client.send_message(message.channel, 'the format for seeing a players bns info is \'!bns (player ign)\'')
		return
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

	"""
	if message.channel.id == '148393296463396864':
		keyw = ['hill','dead','closed','camp','died']
		theM = message.content.split()
		numC = 0
		numT = 0
		timeC = 0
		timeT = None
		wordC = ''
		for i in message.content.lower().split():
			if i in keyw:
				wordC = i
			try:
				if numC < 1:
					testint = int(i)
					numC += 1
					numT = int(i)
			except:
				pass
		for j in message.content.lower().split()[-1]:
			try:
				testint = int(j)
				timeC += 1
			except:
				pass
		if numC > 0 and 'ch' in message.content.lower() and len(wordC) > 0:
			BW = None
			with open("BWinfo.json") as j:
				BW = json.load(j)
				if len(BW["channels"][str(numT)]) == 0 and wordC not in ['hill','camp']:
					if timeC > 1:
						sentence = "CH {}".format((str(numT)+' '+wordC+' '+message.content.lower().split()[-1]))
					else:
						sentence = "CH {}".format((str(numT)+' '+wordC))
					thech = BW["format"][wordC].format(sentence)
					if timeC > 1:
						BW["channels"][str(numT)] = message.content.lower().split()[-1]
					else:
						thetime = str(datetime.now().strftime('%H:%M'))
						BW["channels"][str(numT)] = thetime
			with open('BWinfo.json', 'w') as f:
				json.dump(BW, f, indent = 4)
	"""

	if message.channel.is_private == True and message.author.id != "96763310656983040":
		if newcomes[message.author.id] == 1:
			async def charcheck(msg):
				if namecheck[message.author.id] == None:
					namecheck[message.author.id] = True
					checkM = msg.split()
					if len(checkM) > 1:
						finalM = '%20'.join(checkM)
					else:
						finalM = checkM[0]
					r = requests.get('http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+finalM)
					if len(r.history) == 0:
						from bs4 import BeautifulSoup
						soup = BeautifulSoup(r.text, 'html.parser')
						ncsoftid = soup.find_all(attrs={"class":"signature"})[0].find_all(attrs={"href":"#"})[0].string
						with io.open('BWid.txt','r') as f:
							for name in f:
								if ncsoftid in name:
									await client.send_message(message.author, "Sorry, that ID is already registered, please use another")
									namecheck[message.author.id] = None
									return
						print(ncsoftid)
						await client.send_message(message.author, "Is '{}' your NCSOFT id? Say **yes** or **no** so I can know".format(ncsoftid))
						resp = await client.wait_for_message(timeout = 600, author=message.author)
						if 'n' in resp.content.lower():
							await client.send_message(message.author, "OK, please give me another IGN in your account")
							namecheck[message.author.id] == None
							return
						elif 'y' in resp.content.lower():
							newcomes[message.author.id] += 1
							await client.send_message(message.author, "Alright! I will now add you to the Blackwyrm Discord")
							await client.send_message(discord.utils.get(client.get_all_channels(), id = '148358898024316928'), "Welcome {} to the Discord! They have successfully met the criteria needed to join and will get access soon!".format(message.author.mention))
							with io.open('BWmembers.txt','a') as f:
								writeitdown = message.author.id + ': '+ ncsoftid + ' ['+msg+']\n'
								await client.send_message(discord.utils.get(client.get_all_channels(), id = '148917485297467403'), writeitdown)
								f.write(writeitdown)
							with io.open('BWid.txt','a') as f:
								f.write(ncsoftid+'\n')
							return
						elif resp is None:
							return
					else:
						await client.send_message(message.author, "That character does not exist, please try again.")
						return
			await charcheck(message.content)
		elif BWSecurity["BWpassword"] == message.content and newcomes[message.author.id] < 1:
			print("hello1")
			newcomes[message.author.id] += 1
			await client.send_message(message.author, "That is the correct password!\nNow, please give me the IGN of one of your characters(preferably your main) and I will reply with the NCSOFT id associated with it! Do not impersonate another person! The 10 minute timer still applies, so please dont take too long!")
			#await client.send_message(discord.utils.get(client.get_all_channels(), id = '148358898024316928'), "Welcome {} to the Discord! They have successfully entered the right password! They will get access soon!".format(message.author.mention))
		

"""
@client.event
async def timeloop(t,ch):
	try:
		tTime = datetime.strptime(t, "%H:%M")
	except:
		return
	while len(t) != 0:
		await asyncio.sleep(60)
		mindiff = datetime.now() - tTime
		if mindiff > 58:
			await client.send_message(discord.utils.get(client.get_all_channels(), id = '148358898024316928'), "BW has spawned in channel {}".format(i))
			break
		elif mindiff > 1:
			await client.send_message(discord.utils.get(client.get_all_channels(), id = '148358898024316928'), "BW in channel {} will spawn in less than 5 minutes!".format(i))


with open("BWinfo.json") as j:
	BW = json.load(j)
	async def checkT():
		global BW
		while True:
			for i in BW["channels"]:
				if len(BW["channels"][i]) > 0:
					timeloop(BW["channels"][i], i)
	checkT()
"""




@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	yield from client.change_status(game=discord.Game(name='with no BW zergs'))

def main_task():
	yield from client.login(BWSecurity["user"], BWSecurity["pass"])
	yield from client.connect()

#print(client.user.server.roles)

loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(main_task())
except Exception:
	loop.run_until_complete(client.close())
finally:
	loop.close()
