import requests

def bns(message):
	if len(message.content.split()) == 1:
		return 'the format for seeing a players bns info is \'!bns (player ign)\''
	newerM = message.content.lower()[5:].split()
	if len(newerM) > 1:
		newestM = '%20'.join(newerM)
	else:
		newestM = newerM[0]
	if "faggot" in newestM.lower():
		return 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c=Rain\nhttp://na-bns.ncsoft.com/ingame/bs/character/profile?c=Minko'
	r = requests.get('http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+newestM)
	if len(r.history) == 0:
		finalmessage = 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c={}&s=101'.format(newestM)
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
			hmlevel = soup.find_all(attrs={"class":"signature"})[0].find_all("li")[1].find_all(attrs={"class":"masteryLv"})[0].string.replace("Hongmoon Level", "**Hongmoon Level:**")
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
		finalmessage += "\n**Clan:** {}\n**Class:** {}\n**Level:** {}\n{}\n**Attack:** {}                                                        **HP:** {}\n**Pierce:** {}({})                                          **Defense:** {}({})\n**Accuracy:** {}({})                                 **Evasion:** {}({})\n**Critical Hit:** {}({})                              **Block:** {}({})\n**Critical Damage** {}({})                    **Crit Defense:** {}({})\n".format(clan,classname,level,hmlevel,att,hp,pierce,piercep,defense,defensep,acc,accp,eva,evap,chit,chitp,block,blockp,cdmg,cdmgp,critd,critdp)
		try:
			finalmessage += soup.find_all("div", class_="charaterView")[0].img['src']
		except:
			pass
		return finalmessage
	else:
		return 'Character name does not exist'

def bnstree(message):
	bnsClass = message.content.replace('!bnstree ', '').lower()
	if '!bnstree' == message.content:
		return 'https://bnstree.com/'
	elif 'blade master' == bnsClass or 'bm' == bnsClass:
		return 'https://bnstree.com/BM'
	elif 'kfm' == bnsClass or 'kungfu master' == bnsClass or 'kung fu master' == bnsClass or 'kungfumaster' == bnsClass or 'kf' == bnsClass:
		return 'https://bnstree.com/KF'
	elif 'destroyer' == bnsClass or 'des' == bnsClass or 'de' == bnsClass or 'destro' == bnsClass or 'dest' == bnsClass:
		return 'https://bnstree.com/DE'
	elif 'force master' == bnsClass or 'fm' == bnsClass or 'forcemaster' == bnsClass or 'force user' == bnsClass:
		return 'https://bnstree.com/FM'
	elif 'assassin' == bnsClass or 'as' == bnsClass or 'sin' == bnsClass:
		return 'https://bnstree.com/AS'
	elif 'summoner' == bnsClass or 'su' == bnsClass or 'summ' == bnsClass or 'sum' == bnsClass:
		return 'https://bnstree.com/SU'
	elif 'blade dancer' == bnsClass or 'bd' == bnsClass or 'bladedancer' == bnsClass or 'lbm' == bnsClass or 'lyn blade master' == bnsClass or 'lynblade master' == bnsClass or 'lyn blademaster' == bnsClass:
		return 'https://bnstree.com/BD'
	elif 'warlock' == bnsClass or 'wl' == bnsClass or 'lock' == bnsClass:
		return 'https://bnstree.com/WL'
	elif 'soul fighter' == bnsClass or 'sf' == bnsClass or 'soulfighter' in bnsClass or 'chi master' in bnsClass or 'chimaster' in bnsClass:
		return 'https://bnstree.com/SF'
	else:
		return '2nd argument not recognised'

def savebnsbuild(message):
	if message.content == ('!savebnsbuild') or message.content == ('!savebnsbuild '):
		return 'Your build must contain the format (!savebnsbuild !!(name of command) (tree build url)'
	elif message.content.split()[-1].startswith('https://bnstree.com/') == False:
		return 'Your URL must be from bnstree.com or is missing the https:// prefix'
	elif message.content.split()[1].startswith('!!') == False:
		return 'Your command created command must have !! infront'
	elif len(str(message.content).split()) !=3:
		return 'Can only create a link with exactly 3 arguments'
	elif len(message.content.split()) == 3 and '!!' in message.content.split()[1]: 
		with open('BNSBuilds.txt','r+') as bnsBuilds:
			for line in bnsBuilds:
				if message.content.split()[1] in line:
					return 'A build with this name already exists!'
	bnsBuildsSave = message.content.replace('!savebnsbuild ', '')
	with open('BNSBuilds.txt','a') as bnsBuilds2:
		bnsBuilds2.write(str(message.author.id) + ' ' + bnsBuildsSave + '\n')
		return 'build "'+message.content.split()[2]+'" saved! Use your command "'+message.content.split()[1]+'" to use it!'

def prefixbnscommands(message): # for the !! prefix
	with open('BNSBuilds.txt') as readBuilds:
		for line in readBuilds:
			if message.content.split()[0] == line.split()[1]:
				return line.split()[-1]

def mybnsbuilds(message):
	numbercount = 1
	returnbox = []
	with open('BNSBuilds.txt') as readBuilds:
		for line in readBuilds:
			if str(message.author.id) in line:
				returnbox.append(str(numbercount)+': '+line.replace(str(message.author.id)+ ' ', ''))
				numbercount += 1
	if len(returnbox) == 0:
		return ['You have no saved builds!']
	else:
		return returnbox

def editbnsbuild(message):
	if message.content == ('!editbnsbuild') or message.content == ('!editbnsbuild '):
		return 'Your build must contain the format !editbnsbuild !!(name of command) (tree build url)'
	elif message.content.split()[-1].startswith('https://bnstree.com/') == False:
		return 'Your URL must be from bnstree.com or is missing the https:// prefix'
	if message.content.split()[1].startswith('!!') == False:
		return 'Your edited command must have !! infront'
	if len(str(message.content).split()) !=3:
		return 'Can only edit a link with exactly 3 arguments'
	saveL = ''
	dnBuildsSave = message.content.replace('!editbnsbuild ', '')
	with open('BNSBuilds.txt','r') as bnsBuilds2:
		for line in bnsBuilds2:
			if message.content.split()[1] in line:
				if str(message.author.id) not in line:
					return 'This is not your build so you cannot edit it.'
				elif str(message.author.id) in line:
					saveL = line.rsplit(' ', 1)[0] + ' ' + message.content.split()[-1]
	saveL += '\n'
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
	return 'build "'+message.content.split()[2]+'" has been edited! Use your command "'+message.content.split()[1]+'" to use it!'

def deletebnsbuild(message):
	if message.content == ('!deletebnsbuild') or message.content == ('!deletebnsbuild '):
		return 'Your build must contain the format !deletebnsbuild !!(name of command)'
	elif message.content.split()[1].startswith('!!') == False:
		return 'Your command created command must have !! infront'
	elif len(str(message.content).split()) !=2:
		return 'Can only delete a link with exactly 2 arguments'
	dnBuildsSave = message.content.replace('!deletebnsbuild ', '')
	with open('BNSBuilds.txt','r') as bnsBuilds2:
		for line in bnsBuilds2:
			if message.content.split()[1] in line:
				if str(message.author.id) not in line:
					return 'This is not your build so you cannot delete it.'
	newLines = []
	with open('BNSBuilds.txt','r') as bnsBuilds2:
		for line in bnsBuilds2:
			if message.content.split()[1] not in line:
				newLines.append(line)
	with open('BNSBuilds.txt','w') as bnsBuilds2:
		for line in newLines:
			bnsBuilds2.write(line)
	return 'Your build ' + message.content.split()[-1] + ' has been deleted.'
