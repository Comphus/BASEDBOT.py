import random#idk why this is here

def savednbuild(message):
	if message.content == ('!savednbuild') or message.content == ('!savednbuild '):
		return 'Your build must contain the format !savednbuild $(name of command) (tree build url)'
	elif (message.content.split()[-1].startswith('https://dnss.herokuapp.com') or message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') or message.content.split()[-1].startswith('https://dnmaze.com') or message.content.split()[-1].startswith('http://dnskillsim.herokuapp.com/') or message.content.split()[-1].startswith('https://dnskillsim.herokuapp.com/')) == False:
		return 'Your URL must be from dnskillsim.herokuapp.com,dnss.herokuapp.com, dnss-kr.herokuapp.com or https://dnmaze.com or is missing the https:// prefix'
	elif message.content.split()[1].startswith('$') == False:
		return 'Your command created command must have $ infront'
	elif len(str(message.content).split()) !=3:
		return 'Can only create a link with exactly 3 arguments'
	elif len(message.content.split()) == 3 and '$' in message.content.split()[1]: 
		with open('DNbuilds.txt','r+') as dnBuilds:
			for line in dnBuilds:
				if message.content.lower().split()[1] == line.lower().split()[1]:
					return 'A build with this name already exists!'
	dnBuildsSave = message.content.replace('!savednbuild ', '')
	with open('DNbuilds.txt','a') as bnsBuilds2:
		bnsBuilds2.write(str(message.author.id) + ' ' + dnBuildsSave + '\n')
		return 'build "'+message.content.split()[2]+'" saved! Use your command "'+message.content.split()[1]+'" to use it!'

def prefixdncommands(message): #this is for the $ prefix
	with open('DNbuilds.txt') as readBuilds:
		for line in readBuilds:
			if message.content.split()[0] == line.split()[-2]:
				return line.split()[-1]

def mydnbuilds(message):
	numbercount = 1
	returnbox = []
	with open('DNbuilds.txt') as readBuilds:
		for line in readBuilds:
			if str(message.author.id) in line or str(message.author) in line:
				returnbox.append(str(numbercount)+': '+line.replace(str(message.author.id)+ ' ', ''))
				numbercount += 1
	if len(returnbox) == 0:
		return ['You have no saved builds!']
	else:
		return returnbox

def editdnbuild(message):
	if message.content == ('!editdnbuild') or message.content == ('!editdnbuild '):
		return 'Your build must contain the format !editdnbuild $(name of command) (tree build url)'
	elif (message.content.split()[-1].startswith('https://dnss.herokuapp.com') or message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') or message.content.split()[-1].startswith('https://dnmaze.com') or message.content.split()[-1].startswith('http://dnskillsim.herokuapp.com/') or message.content.split()[-1].startswith('https://dnskillsim.herokuapp.com/')) == False:
		return 'Your URL must be from dnskillsim.herokuapp.com,dnss.herokuapp.com, dnss-kr.herokuapp.com or https://dnmaze.com or is missing the https:// prefix'
	elif len(message.content.split()) == 2 and message.content.split()[1].startswith('$'):
		return 'Your edited command must have $ infront'
	elif len(str(message.content).split()) !=3:
		return 'Can only edit a link with exactly 3 arguments'
	saveL = ''
	dnBuildsSave = message.content.replace('!editdnbuild ', '')
	with open('DNbuilds.txt','r') as bnsBuilds2:
		for line in bnsBuilds2:
			if message.content.split()[1] in line:
				if str(message.author.id) not in line:
					return 'This is not your build so you cannot edit it.'
				elif str(message.author.id) in line:
					saveL = line.rsplit(' ', 1)[0] + ' ' + message.content.split()[-1]
	saveL += '\n'
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
	return 'build "'+message.content.split()[2]+'" has been edited! Use your command "'+message.content.split()[1]+'" to use it!'

def deletednbuild(message):
	if message.content == ('!deletednbuild') or message.content == ('!deletednbuild '):
		return 'Your build must contain the format !deletednbuild $(name of command)'
	if len(message.content.split()) == 2 and message.content.split()[1].startswith('$') == False:
		return 'Your command created command must have $ infront'
	if len(str(message.content).split()) !=2:
		return 'Can only delete a link with exactly 2 arguments'
	with open('DNbuilds.txt','r') as bnsBuilds2:
		for line in bnsBuilds2:
			if message.content.split()[1] in line:
				if str(message.author.id) not in line:
					return 'This is not your build so you cannot delete it.'
	newLines = []
	with open('DNbuilds.txt','r') as bnsBuilds2:
		for line in bnsBuilds2:
			if message.content.split()[1] not in line:
				newLines.append(line)
	with open('DNbuilds.txt','w') as bnsBuilds2:
		for line in newLines:
			bnsBuilds2.write(line)
	return 'Your build ' + message.content.split()[-1] + ' has been deleted.'
