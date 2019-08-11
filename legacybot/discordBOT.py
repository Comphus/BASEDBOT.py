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
logging.basicConfig()

client = discord.Client()
client.login('username', 'password')
client.change_status(587)


with open('twitch.txt') as inputF:
    twitchEmotes = inputF.read().splitlines()

dMods = []
dAdmins = []
with open('Mods.txt','r') as f:
    for i in f:
        dMods.append(str(i).replace('\n', ''))

with open('Admins.txt','r') as f:
    for i in f:
        dAdmins.append(str(i).replace('\n', ''))
        


        

pollStop = ['Comphus']
pollUsers = []
pollStopstr = ''
dTranslate = ''
pollName = ''
ownerName = 'Comphus Arman Donkay'
shutoffName = ['Comphus','Arman','Aelphaeis','Donkay','Hatsune Mikeu','Integration','Voidian']
shutoffCheck = 0

duelCD = 0
duelB = False
timeoutStore = 0
powerTimeout = {}
pmCount = 0
dGamble = {}
timeO = True
dTimeout = {}
firstC = 0
dOut = []
secondC = 0
pollDict = {}
pollResultsKeys = ''
pollResultsValues = ''
countsBNS = 0
pCount = 0
skeleR = 0
counts1 = 0
qQuestion = ['should','can','will','may','are','might','is','do','would','was','am','?','did','how']
gAscend = 0
delayT = 0
commandListts = '''Commands are:\n```!hello\n!donkaysucks\n/lenny\n/shrug\nrandom(space)number\n!randomnumber (lowerlimit) (upperlimit)\n!me(anythinginside)ep\n!duel (2 distinct @ mentions)
!gardenintool\n!retrievename\n!gimmepoutine\n!weary\nvarious mentioning @BASEDBOT commands\n!spookme\n!bnscommands < brings up list of BNS related commands\n!myinfo\n!timeref
all regular twitch emotes(not turbo), a few bttv ones + lirik emotes\n!peoplewithpower\nayy lmao\n!math (whatever math problem)\n!dncommands\n!checktwitch (channelname)\n!avatar (optionalnameofperson, if left blank returns pic of yourself)
Admin only commands:\n!createpoll, format of !createpoll (name) (any number of choices with spaces in between) END <- that tells it youre done making the poll\n!ban (name) fake ban command```
'''
bnsList = '''Commands are for BNS related stuff:\n```!bnstree (can put name of class)\n!savebnsbuild !!(buildname) (URL of build)\n!mybnsbuilds < tells you what builds you made
!editbnsbuild (name of your command) (new build url)\n!deletebnsbuild (name of your command)\n!bnsinfo (ign of someone in bns NA/EU)
```
'''
dnList = '''Commands for DN related stuff:\n```!currentdnupdate\n!currentkdnupdate\n!skillbuilds (can put name of class here)\n!T5skillbuilds (can put name of class here)\n!savednbuild $(buildname) (URL of build)\n!mydnbuilds < tells you what builds you made
!editdnbuild $(name of command) (tree build url)\n!deletednbuild $(name of command)```
'''
magicEight = ['Yes','It is certain','It is decidedly so','Without a doubt','Yes, definitely','You may rely on it','As I see it, yes','Most likely','Outlook good','Signs point to a yes','Reply hazy try again','Ask again later','Better not tell you now','Cannot predict now','Concentrate and ask again','Don\'t count on it','My reply is no','My sources say no','Outlook not so good','Very doubtful']

chatMessage = {'!dncommands':dnList,'!timeref':'1 hour = 3600 seconds\n1 day = 86400 seconds\n1 week = 604800 seconds\n2 weeks = 1209600 seconds','!bnscommands':bnsList,'!commands':commandListts,
'!currentdnupdate':'11/11\nhttp://dragonnest.nexon.net/news/news/00Im3/complete-patch-notes-mists-of-peril','!currentkdnupdate':
'11/11\nhttp://dn.pupugame.com/news/notice.html?mode=read&no=389','/shrug':'¯\ _(ツ)_/¯','!hello':'Hello there!','!donkaysucks':
'Yes, donkay does suck','/lenny':'( ͡° ͜ʖ ͡°)','!gardenintool':'(  ′︵‵  )/',
'!peoplewithpower':'Owner:Comphus\nAdmins: Aelphaeis, Arman, Donkay, Hatsune Mikeu, iCerulean, Integration, Voidian\nChat Moderators: Aggrieved, Maracantress, Marcello, aston, grey, Shs, toto, vara\nForum moderators: Manu, SaitoHikari\nif your name is not on the list but you have one of these roles, PM comphus',}

chatUpload = {'Bob Ross':'BobRoss.jpg','!weary':'weary.jpg','SourPls':'SourPls.jpg','(chompy)':'chompy.jpg','RareParrot':'RareParrot.jpg','RareMing':'RareMing.jpg','PepePls':'PepePls.jpg','(ditto)':'ditto.jpg','!gimmepoutine':'poutine.jpg'}

#the dueling function, takes two mentions to 'duel' against each other. 
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

def skBuilds(dnClass):
    print(dnClass)
    if True == True:
        if True == True:
            if 'gladiator' == dnClass or 'glad' == dnClass:
                return ('https://dnmaze.com/gladiator')
            elif 'lunar knight' == dnClass or 'lk' == dnClass or 'ml' == dnClass or 'moonlord' == dnClass or 'lunarknight' == dnClass or 'moon lord' == dnClass:
                return ('https://dnmaze.com/moonlord')
            elif 'barbarian' == dnClass or 'barb' == dnClass or 'barbie' == dnClass:
                return ('https://dnmaze.com/barbarian')
            elif 'destroyer' == dnClass or 'dest' == dnClass or 'des' == dnClass:
                return ('https://dnmaze.com/destroyer')
            elif 'dark avenger' == dnClass or 'da' == dnClass or 'darkavenger' == dnClass or 'avenger' == dnClass:
                return ('https://dnmaze.com/darkavenger')
            elif 'sniper' == dnClass or 'snipe' == dnClass:
                return ('https://dnmaze.com/sniper')
            elif 'warden' == dnClass or 'arti' == dnClass or 'artillery' == dnClass:
                return ('https://dnmaze.com/artillery')
            elif 'tempest' == dnClass or 'temp' == dnClass:
                return ('https://dnmaze.com/tempest')
            elif 'windwalker' == dnClass or 'ww' == dnClass:
                return ('https://dnmaze.com/windwalker')
            elif 'pyromancer' == dnClass or 'pyro' == dnClass or 'saleana' == dnClass:
                return ('https://dnmaze.com/saleana')
            elif 'ice witch' == dnClass or 'icewitch' == dnClass or 'iw' == dnClass or 'elestra' == dnClass:
                return ('https://dnmaze.com/elestra')
            elif 'war mage' == dnClass or 'warmage' == dnClass or 'wm' == dnClass or 'smasher' == dnClass:
                return ('https://dnmaze.com/smasher')
            elif 'chaos mage' == dnClass or 'chaosmage' == dnClass or 'cm' == dnClass or 'majesty' == dnClass:
                return ('https://dnmaze.com/majesty')
            elif 'guardian' == dnClass or 'guard' == dnClass:
                return ('https://dnmaze.com/guardian')
            elif 'crusader' == dnClass or 'crus' == dnClass or 'sader' == dnClass:
                return ('https://dnmaze.com/crusades')
            elif 'saint' == dnClass:
                return ('https://dnmaze.com/saint')
            elif 'inquisitor' == dnClass or 'inquis' == dnClass:
                return ('https://dnmaze.com/inquisitor')
            elif 'shooting star' == dnClass or 'ss' == dnClass or 'shootingstar' == dnClass:
                return ('https://dnmaze.com/shootingstar')
            elif 'gear master' == dnClass or 'gm' == dnClass or 'gearmaster' == dnClass:
                return ('https://dnmaze.com/gearmaster')
            elif 'adept' == dnClass or 'dept' == dnClass:
                return ('https://dnmaze.com/adept')
            elif 'physician' == dnClass or 'phys' == dnClass:
                return ('https://dnmaze.com/physician')
            elif 'dark summoner' == dnClass or 'ds' == dnClass or 'darksummoner' == dnClass:
                return ('https://dnmaze.com/darksummoner')
            elif 'soul eater' == dnClass or 'se' == dnClass or 'souleater' == dnClass:
                return ('https://dnmaze.com/souleater')
            elif 'blade dancer' == dnClass or 'bd' == dnClass or 'bladedancer' == dnClass:
                return ('https://dnmaze.com/bladedancer')
            elif 'spirit dancer' == dnClass or 'sd' == dnClass or 'spiritdancer' == dnClass:
                return ('https://dnmaze.com/spiritdancer')
            elif 'reaper' == dnClass or 'ripper' == dnClass:
                return ('https://dnmaze.com/ripper')
            elif 'raven' == dnClass:
                return ('https://dnmaze.com/raven')
            elif 'light fury' == dnClass or 'lf' == dnClass or 'light bringer' == dnClass or 'lb' == dnClass or 'lightfury' == dnClass or 'lightbringer' == dnClass:
                return ('https://dnmaze.com/lightfury')
            elif 'abyss walker' == dnClass or 'aw' == dnClass or 'abysswalker' == dnClass:
                return ('https://dnmaze.com/abysswalker')
            elif 'dragoon' == dnClass or 'flurry' == dnClass:
                return ('https://dnmaze.com/flurry')
            elif 'valkyrie' == dnClass or 'sb' == dnClass or 'sting breezer' == dnClass or 'stingbreezer' == dnClass:
                return ('https://dnmaze.com/stingbreezer')
            elif 'ruina' == dnClass:
                return ('https://dnmaze.com/ruina')
            elif 'defensio' == dnClass:
                return ('https://dnmaze.com/defensio')
            else:
                return ('2nd argument not recognised')
                
def kdnBuilds(kdnClass):
    if True == True:
        if True == True:
            if 'gladiator' == kdnClass or 'glad' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/gladiator')
            elif 'lunar knight' == kdnClass or 'lk' == kdnClass or 'ml' == kdnClass or 'moonlord' == kdnClass or 'lunarknight' == kdnClass or 'moon lord' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/moonlord')
            elif 'barbarian' == kdnClass or 'barb' == kdnClass or 'barbie' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/barbarian')
            elif 'destroyer' == kdnClass or 'dest' == kdnClass or 'des' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/destroyer')
            elif 'dark avenger' == kdnClass or 'da' == kdnClass or 'darkavenger' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/darkavenger')
            elif 'sniper' == kdnClass or 'snipe' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/sniper')
            elif 'warden' == kdnClass or 'arti' == kdnClass or 'artillery' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/artillery')
            elif 'tempest' == kdnClass or 'temp' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/tempest')
            elif 'windwalker' == kdnClass or 'ww' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/windwalker')
            elif 'pyromancer' == kdnClass or 'pyro' == kdnClass or 'saleana' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/saleana')
            elif 'ice witch' == kdnClass or 'icewitch' == kdnClass or 'iw' == kdnClass or 'saleana' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/elestra')
            elif 'war mage' == kdnClass or 'warmage' == kdnClass or 'wm' == kdnClass or 'smasher' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/smasher')
            elif 'chaos mage' == kdnClass or 'chaosmage' == kdnClass or 'cm' == kdnClass or 'majesty' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/majesty')
            elif 'guardian' == kdnClass or 'guard' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/guardian')
            elif 'crusader' == kdnClass or 'crus' == kdnClass or 'sader' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/crusades')
            elif 'saint' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/saint')
            elif 'inquisitor' == kdnClass or 'inquis' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/inquisitor')
            elif 'shooting star' == kdnClass or 'ss' == kdnClass or 'shootingstar' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/shootingstar')
            elif 'gear master' == kdnClass or 'gm' == kdnClass or 'gearmaster' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/gearmaster')
            elif 'adept' == kdnClass or 'dept' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/adept')
            elif 'physician' == kdnClass or 'phys' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/physician')
            elif 'dark summoner' == kdnClass or 'ds' == kdnClass or 'darksummoner' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/darksummoner')
            elif 'soul eater' == kdnClass or 'se' == kdnClass or 'souleater' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/souleater')
            elif 'blade dancer' == kdnClass or 'bd' == kdnClass or 'bladedancer' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/bladedancer')
            elif 'spirit dancer' == kdnClass or 'sd' == kdnClass or 'spiritdancer' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/spiritdancer')
            elif 'reaper' == kdnClass or 'ripper' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/ripper')
            elif 'raven' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/raven')
            elif 'light fury' == kdnClass or 'lf' == kdnClass or 'light bringer' == kdnClass or 'lb' == kdnClass or 'lightfury' == kdnClass or 'lightbringer' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/lightfury')
            elif 'abyss walker' == kdnClass or 'aw' == kdnClass or 'abysswalker' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/abysswalker')
            elif 'dragoon' == kdnClass or 'flurry' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/flurry')
            elif 'valkyrie' == kdnClass or 'sb' == kdnClass or 'sting breezer' == kdnClass or 'stingbreezer' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/stingbreezer')
            elif 'defensio' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/defensio')
            elif 'ruina' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/ruina')
            elif 'silver hunter' == kdnClass or 'silverhunter' == kdnClass or 'sh' == kdnClass:
                return ('https://dnss-kr.herokuapp.com/job/silverhunter')
            else:
                return ('2nd argument not recognised')
        

@client.event
def on_member_join(member):
    if str(member.server.id) != '110373943822540800':
        client.send_message(member.server.channels[0], 'Welcome ' + member.mention() + ' to the server!')
        print(member)
        t = datetime.now()
        if str(member.server.id) == '106293726271246336':
            with io.open('joinLog.txt','a',encoding='utf-8') as f:
                retS = ('Name: ' +str(member.name)+ ' ID:' + str(member.id)+ ' Time joined:' + str(t) + ' EST\n')
                f.write(retS)
                

"""
@client.event
def on_status(member):
    t = datetime.now()
    with shelve.open('statUpdate') as db:
        if member.mention() not in db:
            db[member.mention()] = [member.game_id, member.game_id :[t,0]]
        else:
            db[member.mention()][1]statGames[db[member.mention()][0]]
"""

@client.event
def on_message(message):
    global gAscend
    global delayT
    global commandListts
    global magicEight
    global qQuestion
    global counts1
    global skeleR
    global dTranslate
    global twitchEmotes
    global dMods
    global pCount
    global pollDict
    global pollName
    global pollStop
    global pollStopstr
    global pollUsers
    global readPollF
    global chatMessage
    global chatUpload
    global pollResultsKeys
    global pollResultsValues
    global countsBNS
    global shutoffName
    global shutoffCheck
    global someJoinName
    global someJoin
    global dTimeout
    global firstC
    global secondC
    global timeO
    global dGamble
    global pmCount
    global powerTimeout
    global timeoutStore
    global duelCD
    global duelB

    cTime = datetime.now()



    #if 'ouo' in message.content.lower() or 'o u o' in message.content.lower() or 'o  u  o' in message.content.lower() or 'o   u   o' in message.content.lower():
    #    client.delete_message(message)
    if message.content.startswith('!testmentions'):
        client.send_message(message.channel, message.mentions[0].mention())
    """
    if message.content.startswith('!delete ian'):
        with codecs.open('daddy.txt','r',"utf-8") as f:
            for i in f:
                client.send_message(message.channel, i)
                time.sleep(2)
    """
    
    if message.content.startswith('!stopbot') and str(message.author.id) in dMods:
        client.send_message(message.channel, 'Bot has been stopped')
        shutoffCheck = 1
    elif message.content.startswith('!stopbot') and str(message.author.id) not in dMods:
        client.send_message(message.channel, 'You cannot access this command')
    elif message.content.startswith('!startbot') and str(message.author.id) in dMods:
        client.send_message(message.channel, 'Bot has been resumed')
        shutoffCheck = 0
    elif message.content.startswith('!startbot') and str(message.author.id) not in dMods:
        client.send_message(message.channel, 'You cannot access this command')
        """
    if message.mention_everyone:
        newT = cTime.strftime("%H:%M:%S")
        with open('mentionEveryoneLog.txt','a') as m:
            savedMention = str(message.channel.server.name)+'-'+str(message.author) + '-' + str(cTime.strftime("%H:%M:%S"))+': '+str(message.content).replace('@everyone','@-everyone')
            m.write(savedMention+'\n')
    if '<@90886475373109248>' in message.content:
        with open('mentionMeLog.txt','a') as m:
            savedMention = str(message.channel.server.name)+'-'+str(message.author) + '-' + str(cTime.strftime("%H:%M:%S"))+': '+str(message.content).replace('<@90886475373109248>', '@Comphus')
            m.write(savedMention+'\n')
    if message.content.startswith('!mymentions') and str(message.author.id) == '90886475373109248':
        sendingM = 'People who used @-everyone:```\n'
        with codecs.open('mentionEveryoneLog.txt','r',"utf-8") as m:
            for i in m:
                sendingM += i
        sendingM += '```'
        client.send_message(message.channel, sendingM)
        sendingM = 'People who actually @mentioned you:```\n'
        with codecs.open('mentionMeLog.txt','r',"utf-8") as m:
            for i in m:
                sendingM += i
        sendingM +='```'
        client.send_message(message.channel, sendingM)
    if message.content.startswith('!clearmentions') and str(message.author.id) == '90886475373109248':
        codecs.open('mentionEveryoneLog.txt', 'w',"utf-8").close()
        codecs.open('mentionMeLog.txt', 'w',"utf-8").close()
        client.send_message(message.channel, 'Done')
        """

    if message.content.startswith('!joinlog') and str(message.channel.id) == '106301620500836352':
        with codecs.open('joinLog.txt','r','utf-8') as s:
            logM = []
            tempL = ''
            for line in s:
                tempL += line.replace('\n', '')
                if len(tempL) > 1800:
                    logM.append(tempL)
                    tempL = ''
            logM.append(tempL)
            for i in logM:
                client.send_message(message.channel, 'List of people who joined the server:\n\n' + i)
        
        
        
            
    if message.content.startswith('!serverpic'):
        client.send_message(message.channel, message.channel.server.icon_url())
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
        client.add_roles(message.mentions[0], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
        client.send_message(message.channel, newM[1]+' has been timed out for '+newM[2]+' seconds.')
    elif message.content.startswith('!timeout') and str(message.author.id) in dAdmins:
        client.send_message(message.channel, 'The format for timing someone out is !timeout @ mention (timeinseconds)')
    if message.content.startswith('!stoptimeout') and str(message.author.id) in dAdmins and len(message.content.split()) == 2:
        newM = message.content.split()
        if newM[1] in powerTimeout:
            client.remove_roles(powerTimeout[newM[1]][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
            powerTimeout.pop(newM[1])
            client.send_message(message.channel, newM[1]+'\'s timeout has been manually stopped.')
        elif 'Jail' in discord.utils.find(lambda m: m.name == 'Jail', message.channel.server.members).roles:
            client.remove_roles(powerTimeout[newM[1]][2], discord.utils.find(lambda r: r.name == 'Jail', message.channel.server.roles))
            client.send_message(message.channel, newM[1]+'\'s timeout has been manually stopped.')
        else:
            client.send_message(message.channel, 'That person has not been manually timed out.')
    elif message.content.startswith('!stoptimeout') and str(message.author.id) in dAdmins:
        client.send_message(message.channel, 'The format for timing someone out is !timeout @ mention')

        
    if len(message.content) > 0 and message.channel.is_private == False and message.author.mention() not in powerTimeout.keys() and str(message.author.id) != '106469383206883328':
        mId = str(message.author.id)
        t1 = datetime.now()
        if mId in dTimeout:
            dTimeout[mId][1] = t1
            tDiff = dTimeout[mId][1] - dTimeout[mId][0]
            dTimeout[mId][2] += 1
            if dTimeout[mId][4] == str(message.content):
                dTimeout[mId][5] += 1
            dTimeout[mId][4] = str(message.content)
            if tDiff.seconds >= 3:
                if mId == '106469383206883328':
                    if dTimeout[mId][2] > 9 or dTimeout[mId][5] > 4:
                        dTimeout[mId][-1] = 10
                        dTimeout[mId][1] = t1
                        if dTimeout[mId][3] == True:
                            client.send_message(message.channel, 'I have timed myself out for 30 seconds due to spamming.')
                            dTimeout[mId][3] = False
                elif dTimeout[mId][2] > 6 and str(message.channel.server.id) not in '110373943822540800 90981699927670784':
                    dTimeout[mId][-1] = 1
                    dTimeout[mId][1] = t1
                    if dTimeout[mId][3] == True:
                        client.send_message(message.channel, str(message.author)+' has been timed out for 30 seconds for spamming.')
                        dTimeout[mId][3] = False
                elif dTimeout[mId][5] > 2 and str(message.channel.server.id) not in '110373943822540800 90981699927670784':
                    dTimeout[mId][-1] = 1
                    dTimeout[mId][1] = t1
                    if dTimeout[mId][3] == True:
                        client.send_message(message.channel, str(message.author)+' has been timed out for 30 seconds for spamming the same word.')
                        dTimeout[mId][3] = False
                else:
                    dTimeout[mId][0] = t1
                    dTimeout[mId][1] = t1
                    dTimeout[mId][2] = 0
                    dTimeout[mId][3] = True
                    dTimeout[mId][4] = ''
                    dTimeout[mId][5] = 0
                    dTimeout[mId][-1] = 0
            if tDiff.seconds >= 33:
                dTimeout[mId][0] = t1
                dTimeout[mId][1] = t1
                dTimeout[mId][2] = 0
                if dTimeout[mId][3] == False:
                    client.send_message(message.channel, str(message.author)+'\'s timeout has been lifted.')
                    dTimeout[mId][3] = True
                dTimeout[mId][4] = ''
                dTimeout[mId][5] = 0
                dTimeout[mId][-1] = 0        
    if str(message.author.id) not in dTimeout:
        t1 = datetime.now()
        dTimeout[str(message.author.id)] = [t1,t1,0,True,'',0,0]
        
    if dTimeout[str(message.author.id)][-1] == 1 and shutoffCheck == 0:
        client.delete_message(message)
    elif dTimeout[str(message.author.id)][-1] == 10:
        if message.content != 'I have timed myself out for 30 seconds due to spamming.':
            client.delete_message(message)
    elif shutoffCheck == 0 and message.author.mention() not in powerTimeout.keys():
        if message.content.startswith('!serverid'):
            client.send_message(message.channel, message.channel.server.id)
        if message.content.startswith('!say') and str(message.author.id) == '90886475373109248':
            nM = message.content.replace('!say ', '')
            client.send_message(message.channel, nM)
        if message.content.startswith('!duel') and str(message.channel.id) not in '91518345953689600':
            if len(message.mentions) != 2:
                client.send_message(message.channel, 'Must have only two distinct mentions.')
            elif message.mentions[0].mention() == message.mentions[1].mention():
                client.send_message(message.channel, 'Must have two distinct mentions.')
            elif str(message.channel.id) == '106293726271246336':
                if duelB == False:
                    results = dueling([message.mentions[0].mention(),message.mentions[1].mention()])
                    client.send_message(message.channel, results[1])
                    for i in range(len(results[0])):
                        client.send_message(message.channel, results[0][i])
                        client.send_message(message.channel, results[2]+'\n')
                                            
                if duelCD == 0:
                    duelCD = cTime
                    duelB = True
                timeR = cTime - duelCD
                if timeR.seconds < 300:
                    
                    client.send_message(message.channel, 'Dueling is currently on CD, has '+str(300-timeR.seconds)+' seconds left')
                elif timeR >= 300:
                    client.send_message(message.channel, 'Dueling CD has finished, do !duel again to duel')
                    duelCD = 0
                    duelB = False

                    
            else:
                results = dueling([message.mentions[0].mention(),message.mentions[1].mention()])
                client.send_message(message.channel, results[1])
                for i in range(len(results[0])):
                    client.send_message(message.channel, results[0][i])
                    client.send_message(message.channel, results[2])

        #print(str(message.author.id))
        #print(dMods)
        #print(str(90886475373109248) in dMods)
        for i in chatMessage:
            if i in message.content:
                client.send_message(message.channel, chatMessage[message.content.split()[0]])
                time.sleep(delayT)
                pmCount = 1
        for i in chatUpload:
            if i in message.content:
                try:
                    client.send_file(message.channel, chatUpload[message.content.split()[0]])
                except IndexError:
                    print('')
                time.sleep(delayT)
                pmCount = 1
        if message.content.startswith('!chid'):
            client.send_message(message.channel, message.channel.id)
            pmCount = 1
        if message.content.startswith('!bnsinfo') and len(message.content.split()) > 1:
            newM = message.content.lower()[9:]
            newerM = newM.split()
            if len(newerM) > 1:
                newestM = '%20'.join(newerM)
            else:
                newestM = newerM[0]
            r = requests.get('http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+newestM+'&s=101')
            if len(r.history) == 0:
                client.send_message(message.channel, 'http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+newestM+'&s=101')
                from selenium import webdriver
                br = webdriver.PhantomJS()
                br.get('http://na-bns.ncsoft.com/ingame/bs/character/profile?c='+newestM+'&s=101')
                br.save_screenshot('BNSstatshot.jpg')
                br.quit
                client.send_file(message.channel, 'BNSstatshot.jpg')
            else:
                client.send_message(message.channel, 'Character name does not exist')
        if message.content.startswith('!bnsinfo') and len(message.content.split()) == 1:
            client.send_message(message.channel, 'the format for seeing a players bns info is \'!bnsinfo (player ign)\'')
            """
        if message.content.startswith('!gamble') and str(message.channel.id) in '112810780532944896 112185703961534464':
            newG = message.content.split()
            if len(newG) == 1:
                gamb = random.randint(-100,100)
                i = str(message.author.id)
                if i not in dGamble:
                    dGamble[i] = 500
                    client.send_message(message.channel, 'Created account with 500 credits!')
                else:
                    dGamble[i] += gamb
                    client.send_message(message.channel, 'You rolled a {}, your score is now {}.'.format(int(gamb),dGamble[i]))
                    if dGamble[i] < 1:
                        client.send_message(message.channel, 'You lost! Your credits have been reset. '+message.author.mention())
                        dGamble[i] = 500
                        
                    if dGamble[i] > 999:
                        client.send_message(message.channel, 'You won!  Your credits have been reset. '+message.author.mention())
                        dGamble[i] = 500             
            elif len(message.content.split()) == 2:
                rollNum = int(newG[1])
                for z in range(rollNum):
                    gamb = random.randint(-100,100)
                    i = str(message.author.id)
                    if i not in dGamble:
                        dGamble[i] = 500
                        client.send_message(message.channel, 'Created account with 500 credits!')
                    else:
                        dGamble[i] += gamb
                        client.send_message(message.channel, 'You rolled a {}, your score is now {}.'.format(int(gamb),dGamble[i]))
                        if dGamble[i] < 1:
                            client.send_message(message.channel, 'You lost! Your credits have been reset. That took '+str(z)+' tries! '+message.author.mention())
                            dGamble[i] = 500
                            break
                        if dGamble[i] > 999:
                            client.send_message(message.channel, 'You won!  Your credits have been reset. That took '+str(z)+' tries! '+message.author.mention())
                            dGamble[i] = 500
                            break
                """
        if message.content.startswith('!pugs') and str(message.channel.id) == '106300530548039680' and len(message.content.split()) > 1 and str(message.channel.server.id) == '106293726271246336' and message.mention_everyone == False:
            pugM = 'Topic is:\n'
            pugM += message.content[6:]
            if len(message.mentions) != 0:
                for i in message.mentions:
                    pugM = pugM.replace(i.mention(), '-No mentions-')
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
                    client.send_message(message.channel, pugM + '\n\n' + i)
        elif message.content.startswith('!pugs') and str(message.channel.id) != '106300530548039680' and str(message.channel.server.id) == '106293726271246336':
            client.send_message(message.channel, 'You can only call for pugs in the <#106300530548039680> channel.')
        elif message.content.startswith('!pugs') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
            client.send_message(message.channel, 'You must have a topic to tell the people about what you are recruiting them for. It is BANNABLE if you do not have a legitamate topic on purpose.')
        elif message.content.lower().startswith('!pug') and str(message.channel.server.id) == '106293726271246336':
            pugL = ''
            with open('puglist.txt','r') as s:
                pugL = s.read()
            if message.author.mention() not in pugL:
                with open('puglist.txt','a') as s:
                    s.write(message.author.mention())
                    s.write('\n')
                    client.send_message(message.channel, 'You have successfully signed up for pug mentions.')
            if message.author.mention() in pugL:
                newL = []
                with open('puglist.txt','r') as s:
                    for line in s:
                        if message.author.mention() not in line:
                            newL.append(line)
                with open('puglist.txt','w') as s:
                    for line in newL:    
                        s.write(line)
                client.send_message(message.channel, 'You have successfully removed yourself for pug mentions.')

        if message.content.startswith('!test'):
            client.send_message(message.channel, '<@90886475373109248>', mentions = True)
        if message.content.startswith('!trades') and str(message.channel.id) == '106301265817931776' and len(message.content.split()) > 1 and str(message.channel.server.id) == '106293726271246336' and message.mention_everyone == False:
            tradeM = 'Topic is:\n'
            tradeM += message.content[8:]
            if len(message.mentions) != 0:
                for i in message.mentions:
                    tradeM = tradeM.replace(i.mention(), '-No mentions-')
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
                    client.send_message(message.channel, tradeM + '\n\n' + i)
        elif message.content.startswith('!trades') and str(message.channel.id) != '106301265817931776' and str(message.channel.server.id) == '106293726271246336':
            client.send_message(message.channel, 'You can only call for trades in the <#106301265817931776> channel.')
        elif message.content.startswith('!trades') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
            client.send_message(message.channel, 'You must have a topic to tell the people about what you want to trade. It is BANNABLE if you do not have a legitamate topic on purpose.')
        elif message.content.lower().startswith('!trade') and str(message.channel.server.id) == '106293726271246336':
            tradeL = ''
            with open('tradelist.txt','r') as s:
                tradeL = s.read()
            if message.author.mention() not in tradeL:
                with open('tradelist.txt','a') as s:
                    s.write(message.author.mention())
                    s.write('\n')
                    client.send_message(message.channel, 'You have successfully signed up for trade mentions.')
            if message.author.mention() in tradeL:
                newL = []
                with open('tradelist.txt','r') as s:
                    for line in s:
                        if message.author.mention() not in line:
                            newL.append(line)
                with open('tradelist.txt','w') as s:
                    for line in newL:    
                        s.write(line)
                client.send_message(message.channel, 'You have successfully removed yourself for trade mentions.')

        if message.content.startswith('!pvping') and str(message.channel.id) == '106300621459628032' and len(message.content.split()) > 1 and str(message.channel.server.id) == '106293726271246336' and message.mention_everyone == False:
            pvpM = 'Topic is:\n'
            pvpM += message.content[8:]
            if len(message.mentions) != 0:
                for i in message.mentions:
                    pvpM = pvpM.replace(i.mention(), '-No mentions-')
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
                    client.send_message(message.channel, pvpM + '\n\n' + i)
        elif message.content.startswith('!pvping') and str(message.channel.id) != '106300621459628032' and str(message.channel.server.id) == '106293726271246336':
            client.send_message(message.channel, 'You can only call for pvp in the <#106300621459628032> channel.')
        elif message.content.startswith('!pvping') and len(message.content.split()) < 2 and str(message.channel.server.id) == '106293726271246336':
            client.send_message(message.channel, 'You must have a topic to tell the people about your pvp request. It is BANNABLE if you do not have a legitamate topic on purpose.')
        elif message.content.lower().startswith('!pvp') and str(message.channel.server.id) == '106293726271246336':
            pvpL = ''
            with open('pvplist.txt','r') as s:
                pvpL = s.read()
            if message.author.mention() not in pvpL:
                with open('pvplist.txt','a') as s:
                    s.write(message.author.mention())
                    s.write('\n')
                    client.send_message(message.channel, 'You have successfully signed up for pvp mentions.')
            if message.author.mention() in pvpL:
                newL = []
                with open('pvplist.txt','r') as s:
                    for line in s:
                        if message.author.mention() not in line:
                            newL.append(line)
                with open('pvplist.txt','w') as s:
                    for line in newL:    
                        s.write(line)
                client.send_message(message.channel, 'You have successfully removed yourself for pvp mentions.')
                
            
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
                        client.send_message(message.channel, tChan+'\'s channel is currently offline!')
                    else:
                        client.send_message(message.channel, tChan+'\'s channel is currently offline!')
                else:
                    if tChan == 'jaesung':
                        tChan = 'lsjjws3'
                        client.send_message(message.channel, tChan+'\'s channel is currently online!')
                        client.send_message(message.channel, tChan+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+tChan))
                    else:
                        client.send_message(message.channel, tChan+'\'s channel is currently online!')
                        client.send_message(message.channel, tChan+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+tChan))
            elif r.status_code == 404:
                client.send_message(message.channel, 'This channel does not exist.')
            elif r.status_code == 422:
                client.send_message(message.channel, 'Channel ' + tChan + ' is a justin.tv channel and doesnt work on twitch or is banned!')
            pmCount = 1
        elif message.content.startswith('!checktwitch') and len(message.content.split()) == 1:
            client.send_message(message.channel, 'The format of !checktwitch is !checktwitch (channelname).')
            pmCount = 1
        elif message.content.startswith('!checktwitch') and len(message.content.split()) > 2:
            client.send_message(message.channel, 'The !checktwitch function only takes 1 argument!')
            pmCount = 1
            """
        if message.content.startswith('!createpoll') and str(message.author.id) in dMods and pCount == 0:
            pMessage = message.content.replace('!createpoll ', '')
            newP = pMessage.split()
            countforpoll = 0
            for p in newP:
                if countforpoll == 0:
                    countforpoll = 1
                    pollName = p
                elif 'END' != p:
                    pollDict[p] = 0
            pCount = 1
            pollStop.append(message.author.id)
            pollStopstr = str(message.author.id)
            client.send_message(message.channel, 'Poll "'+pollName+'" was created!')
            pollHelp = []
            pollHelp2 = ''
            for i in pollDict.keys():
                pollHelp.append('('+i+')')
            for i in pollHelp:
                pollHelp2 += i
                if i != pollHelp[-1]:
                    pollHelp2 += ' or '
            client.send_message(message.channel, 'In order to enter, type in ' + pollHelp2 + ' with a "!" infront of it to enter! You only get 1 vote per poll, no retakes!\nPoll creator may !endpoll to end the poll at any time')
            pmCount = 1
        elif message.content.startswith('!createpoll') and str(message.author.id) not in dMods:
            client.send_message(message.channel, 'You do not have permission to access this command')
            time.sleep(delayT)
            pmCount = 1
        elif message.content.startswith('!createpoll') and str(message.author.id) in dMods and pCount == 1:
            client.send_message(message.channel, 'There is already an active poll, only 1 poll at a time')
            time.sleep(delayT)
            pmCount = 1
        if pCount == 1 and message.content.startswith('!'):
            if message.content.replace('!', '') in pollDict and str(message.author.id) not in pollUsers:
                pollDict[message.content.replace('!','')] += 1
                pollUsers.append(str(message.author.id))
                client.send_message(message.channel, 'You have voted "'+message.content.replace('!','')+'"!')
            elif str(message.author.id) in pollUsers:
                client.send_message(message.channel, 'You have already voted!')
            pmCount = 1
        if message.content.startswith('!endpoll') and str(message.author.id) in dAdmins and pCount == 1:
            for pKeys in pollDict.keys():
                pollResultsKeys += pKeys + ' '
            for pVals in pollDict.values():
                pollResultsValues += str(pVals) + '-'    
            client.send_message(message.channel, 'The results of the poll "'+ pollName  + '" are:\n' + pollResultsKeys + '\n' + pollResultsValues[:-1])
            pollStop.remove(str(message.author.id))
            pollStopstr = ''
            pollResults = ''
            pollName = ''
            pollResultsKeys = ''
            pollResultsValues = ''
            pollUsers = []
            pollHelp = []
            pollHelp2 = ''
            pollDict = {}
            pCount = 0
            pmCount = 1
        elif message.content.startswith('!endpoll') and str(message.author.id) in pollStop and pCount == 1:
            for pKeys in pollDict.keys():
                pollResultsKeys += pKeys + ' '
            for pVals in pollDict.values():
                pollResultsValues += str(pVals) + '-'    
            client.send_message(message.channel, 'The results of the poll "'+ pollName  + '" are:\n' + pollResultsKeys + '\n' + pollResultsValues[:-1])
            pollStop.remove(str(message.author.id))
            pollStopstr = ''
            pollResults = ''
            pollName = ''
            pollResultsKeys = ''
            pollResultsValues = ''
            pollUsers = []
            pollHelp = []
            pollHelp2 = ''
            pollDict = {}
            pCount = 0
            pmCount = 1
            """
        
            
        if str(message.content).count('┻') > 1:
            t = int(str(message.content).count('┻')/2)
            client.send_message(message.channel, '┬─┬ ノ( ^_^ノ) '* t)
            pmCount = 1
        if 'beat the devil out of it' in message.content.lower():
            client.send_file(message.channel, 'bobrossbeat.jpg')
            pmCount = 1
        if 'i made a mistake' in message.content.lower():
            client.send_file(message.channel, 'bobrossmistake.jpg')
            pmCount = 1
            
        if message.content.startswith('~coin'):
            if random.randint(0,1) == 0:
                client.send_message(message.channel, message.author.mention() + ' `throws a coin`: tails!')
            else:
                client.send_message(message.channel, message.author.mention() + ' `throws a coin`: heads!')
                

            
        if message.content.lower().startswith('!skillbuilds'):
            dnClass = message.content.lower().replace('!skillbuilds ', '')
            if '!skillbuilds' == str(message.content).lower() or '!skillbuilds ' == str(message.content).lower():
                client.send_message(message.channel, 'http://dnmaze.com/')
            else:
                client.send_message(message.channel, skBuilds(dnClass))
            pmCount = 1

        if message.content.startswith('!thetatat'):
            with open('skillbuildcode.txt') as r:
                s = r.read().replace('client.send_message(message.channel, ', 'return (')
                s = s.replace('dnClass', 'kdnClass')
                print(s)
                
        if message.content.lower().startswith('!t5skillbuilds'):
            dnClass = message.content.lower().replace('!t5skillbuilds ', '')
            if '!t5skillbuilds' == str(message.content).lower() or '!t5skillbuilds ' == str(message.content).lower():
                client.send_message(message.channel, 'https://dnss-kr.herokuapp.com/')
            else:
                client.send_message(message.channel, kdnBuilds(dnClass))
            pmCount = 1
        if message.content.startswith('!savednbuild'):
            print(message.content.split()[-1])
            print(message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com'))
            if message.content == ('!savednbuild') or message.content == ('!savednbuild ') and countsBNS == 0:
                client.send_message(message.channel, 'Your build must contain the format !savednbuild $(name of command) (tree build url)')
                countsBNS = 1
            if message.content.split()[-1].startswith('https://dnss.herokuapp.com') == False and countsBNS == 0:
                if message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') == False and countsBNS == 0:
                    if message.content.split()[-1].startswith('https://dnmaze.com') == False and countsBNS == 0:
                        client.send_message(message.channel, 'Your URL must be from dnss.herokuapp.com, dnss-kr.herokuapp.com or https://dnmaze.com or is missing the https:// prefix')
                        countsBNS = 1
            if message.content.split()[1].startswith('$') == False and countsBNS == 0:
                client.send_message(message.channel, 'Your command created command must have $ infront')
                countsBNS = 1
            if len(str(message.content).split()) !=3 and countsBNS == 0:
                client.send_message(message.channel, 'Can only create a link with exactly 3 arguments')
                countsBNS = 1
            if len(message.content.split()) == 3 and '$' in message.content.split()[1] and countsBNS == 0: 
                with open('DNbuilds.txt','r+') as dnBuilds:
                    for line in dnBuilds:
                        if message.content.split()[1] in line:
                            client.send_message(message.channel, 'A build with this name already exists!')
                            countsBNS = 1
            if countsBNS == 0:
                dnBuildsSave = message.content.replace('!savednbuild ', '')
                with open('DNbuilds.txt','a') as bnsBuilds2:
                    bnsBuilds2.write(str(message.author.id) + ' ' + dnBuildsSave + '\n')
                    client.send_message(message.channel, 'build "'+message.content.split()[2]+'" saved! Use your command "'+message.content.split()[1]+'" to use it!')
            countsBNS = 0
            pmCount = 1
        if message.content.startswith('$') and counts1 == 0:
            with open('DNbuilds.txt') as readBuilds:
                for line in readBuilds:
                    if message.content.split()[0] == line.split()[-2]:
                        client.send_message(message.channel, line.split()[-1])
                        counts1 = 1
            counts1 = 0
            pmCount = 1
        if message.content.startswith('!mydnbuilds'):
            tempCount = 1
            with open('DNbuilds.txt') as readBuilds:
                for line in readBuilds:
                    if str(message.author.id) in line or str(message.author) in line:
                        client.send_message(message.channel, str(tempCount)+': '+line.replace(str(message.author.id)+ ' ', ''))
                        tempCount += 1
            if tempCount == 1:
                client.send_message(message.channel, 'You have no saved builds!')
            pmCount = 1
        if message.content.startswith('!editdnbuild'):
            if message.content == ('!editdnbuild') or message.content == ('!editdnbuild ') and countsBNS == 0:
                client.send_message(message.channel, 'Your build must contain the format !editdnbuild $(name of command) (tree build url)')
                countsBNS = 1
            if message.content.split()[-1].startswith('https://dnss.herokuapp.com') == False and countsBNS == 0:
                if message.content.split()[-1].startswith('https://dnss-kr.herokuapp.com') == False and countsBNS == 0:
                    if message.content.split()[-1].startswith('https://dnmaze.com') == False and countsBNS == 0:
                        client.send_message(message.channel, 'Your URL must be from dnss.herokuapp.com ,dnss-kr.herokuapp.com or http://dnmaze.com/ or is missing the http(s):// prefix')
                        countsBNS = 1
            if message.content.split()[1].startswith('$') == False and countsBNS == 0:
                client.send_message(message.channel, 'Your edited command must have $ infront')
                countsBNS = 1
            if len(str(message.content).split()) !=3 and countsBNS == 0:
                client.send_message(message.channel, 'Can only edit a link with exactly 3 arguments')
                countsBNS = 1
            if countsBNS == 0:
                saveL = ''
                dnBuildsSave = message.content.replace('!editdnbuild ', '')
                with open('DNbuilds.txt','r') as bnsBuilds2:
                    for line in bnsBuilds2:
                        if message.content.split()[1] in line:
                            if str(message.author.id) not in line:
                                client.send_message(message.channel, 'This is not your build so you cannot edit it.')
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
                    client.send_message(message.channel, 'build "'+message.content.split()[2]+'" has been edited! Use your command "'+message.content.split()[1]+'" to use it!')
            countsBNS = 0
            pmCount = 1
        
        if message.content.startswith('!deletednbuild'):
            if message.content == ('!deletednbuild') or message.content == ('!deletednbuild ') and countsBNS == 0:
                client.send_message(message.channel, 'Your build must contain the format !deletednbuild $(name of command)')
                countsBNS = 1
            if message.content.split()[1].startswith('$') == False and countsBNS == 0:
                client.send_message(message.channel, 'Your command created command must have $ infront')
                countsBNS = 1
            if len(str(message.content).split()) !=2 and countsBNS == 0:
                client.send_message(message.channel, 'Can only delete a link with exactly 2 arguments')
                countsBNS = 1
            if countsBNS == 0:
                dnBuildsSave = message.content.replace('!deletednbuild ', '')
                with open('DNbuilds.txt','r') as bnsBuilds2:
                    for line in bnsBuilds2:
                        if message.content.split()[1] in line:
                            if str(message.author.id) not in line:
                                client.send_message(message.channel, 'This is not your build so you cannot delete it.')
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
                    client.send_message(message.channel, 'Your build ' + message.content.split()[-1] + ' has been deleted.')
            pmCount = 1
        if message.content.startswith('!bnstree'):
            bnsClass = message.content.replace('!bnstree ', '').lower()
            if '!bnstree' == message.content:
                client.send_message(message.channel, 'https://bnstree.com/')
            elif 'blade master' == bnsClass or 'bm' == bnsClass:
                client.send_message(message.channel, 'https://bnstree.com/BM')
            elif 'kfm' == bnsClass or 'kungfu master' == bnsClass or 'kung fu master' == bnsClass or 'kungfumaster' == bnsClass or 'kf' == bnsClass:
                client.send_message(message.channel, 'https://bnstree.com/KF')
            elif 'destroyer' == bnsClass or 'des' == bnsClass or 'de' == bnsClass or 'destro' == bnsClass or 'dest' == bnsClass:
                client.send_message(message.channel, 'https://bnstree.com/DE')
            elif 'force master' == bnsClass or 'fm' == bnsClass or 'forcemaster' == bnsClass or 'force user' == bnsClass:
                client.send_message(message.channel, 'https://bnstree.com/FM')
            elif 'assassin' == bnsClass or 'as' == bnsClass or 'sin' == bnsClass:
                client.send_message(message.channel, 'https://bnstree.com/AS')
            elif 'summoner' == bnsClass or 'su' == bnsClass or 'summ' == bnsClass or 'sum' == bnsClass:
                client.send_message(message.channel, 'https://bnstree.com/FM')
            elif 'blade dancer' == bnsClass or 'bd' == bnsClass or 'bladedancer' == bnsClass or 'lbm' == bnsClass or 'lyn blade master' == bnsClass or 'lynblade master' == bnsClass or 'lyn blademaster' == bnsClass:
                client.send_message(message.channel, 'https://bnstree.com/BD')
            elif 'warlock' == bnsClass or 'wl' == bnsClass or 'lock' == bnsClass:
                client.send_message(message.channel, 'https://bnstree.com/WL')
            else:
                client.send_message(message.channel, '2nd argument not recognised')
            pmCount = 1
        if message.content.startswith('!savebnsbuild'):
            if message.content == ('!savebnsbuild') or message.content == ('!savebnsbuild '):
                client.send_message(message.channel, 'Your build must contain the format (!savebnsbuild !!(name of command) (tree build url)')
                countsBNS = 1
            elif message.content.split()[-1].startswith('https://bnstree.com/') == False:
                client.send_message(message.channel, 'Your URL must be from bnstree.com or is missing the https:// prefix')
                countsBNS = 1
            elif message.content.split()[1].startswith('!!') == False:
                client.send_message(message.channel, 'Your command created command must have !! infront')
                countsBNS = 1
            elif len(str(message.content).split()) !=3:
                client.send_message(message.channel, 'Can only create a link with exactly 3 arguments')
                countsBNS = 1
            elif len(message.content.split()) == 3 and '!!' in message.content.split()[1]: 
                with open('BNSBuilds.txt','r+') as bnsBuilds:
                    for line in bnsBuilds:
                        if message.content.split()[1] in line:
                            client.send_message(message.channel, 'A build with this name already exists!')
                            countsBNS = 1
            if countsBNS == 0:
                bnsBuildsSave = message.content.replace('!savebnsbuild ', '')
                with open('BNSBuilds.txt','a') as bnsBuilds2:
                    bnsBuilds2.write(str(message.author.id) + ' ' + bnsBuildsSave + '\n')
                    client.send_message(message.channel, 'build "'+message.content.split()[2]+'" saved! Use your command "'+message.content.split()[1]+'" to use it!')
            countsBNS = 0
            pmCount = 1
        if message.content.startswith('!!') and counts1 == 0:
            with open('BNSBuilds.txt') as readBuilds:
                for line in readBuilds:
                    if message.content.split()[0] == line.split()[1]:
                        client.send_message(message.channel, line.split()[-1])
                        counts1 = 1
            counts1 = 0
            pmCount = 1
        
        if message.content.startswith('!mybnsbuilds'):
            tempCount = 1
            with open('BNSBuilds.txt') as readBuilds:
                for line in readBuilds:
                    if str(message.author.id) in line:
                        client.send_message(message.channel, str(tempCount)+': '+line.replace(str(message.author.id)+ ' ', ''))
                        tempCount += 1
            if tempCount == 1:
                client.send_message(message.channel, 'You have no saved builds!')
            pmCount = 1
            
        if message.content.startswith('!editbnsbuild'):
            if message.content == ('!editbnsbuild') or message.content == ('!editbnsbuild ') and countsBNS == 0:
                client.send_message(message.channel, 'Your build must contain the format !editbnsbuild !!(name of command) (tree build url)')
                countsBNS = 1
            elif message.content.split()[-1].startswith('https://bnstree.com/') == False and countsBNS == 0:
                client.send_message(message.channel, 'Your URL must be from dnss.herokuapp.com ,dnss-kr.herokuapp.com or http://dnmaze.com/ or is missing the http(s):// prefix')
                countsBNS = 1
            if message.content.split()[1].startswith('!!') == False and countsBNS == 0:
                client.send_message(message.channel, 'Your edited command must have !! infront')
                countsBNS = 1
            if len(str(message.content).split()) !=3 and countsBNS == 0:
                client.send_message(message.channel, 'Can only edit a link with exactly 3 arguments')
                countsBNS = 1
            if countsBNS == 0:
                saveL = ''
                dnBuildsSave = message.content.replace('!editbnsbuild ', '')
                with open('BNSBuilds.txt','r') as bnsBuilds2:
                    for line in bnsBuilds2:
                        if message.content.split()[1] in line:
                            if str(message.author.id) not in line:
                                client.send_message(message.channel, 'This is not your build so you cannot edit it.')
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
                    client.send_message(message.channel, 'build "'+message.content.split()[2]+'" has been edited! Use your command "'+message.content.split()[1]+'" to use it!')
            countsBNS = 0
            pmCount = 1
        
        if message.content.startswith('!deletebnsbuild'):
            if message.content == ('!deletebnsbuild') or message.content == ('!deletebnsbuild '):
                client.send_message(message.channel, 'Your build must contain the format !deletebnsbuild !!(name of command)')
                countsBNS = 1
            elif message.content.split()[1].startswith('!!') == False:
                client.send_message(message.channel, 'Your command created command must have !! infront')
                countsBNS = 1
            elif len(str(message.content).split()) !=2:
                client.send_message(message.channel, 'Can only delete a link with exactly 2 arguments')
                countsBNS = 1
            elif countsBNS == 0:
                dnBuildsSave = message.content.replace('!deletebnsbuild ', '')
                with open('BNSBuilds.txt','r') as bnsBuilds2:
                    for line in bnsBuilds2:
                        if message.content.split()[1] in line:
                            if str(message.author.id) not in line:
                                client.send_message(message.channel, 'This is not your build so you cannot delete it.')
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
                    client.send_message(message.channel, 'Your build ' + message.content.split()[-1] + ' has been deleted.')
            pmCount = 1
            countsBNS = 0
            
        if message.content.startswith('!myid'):
            client.send_message(message.channel, message.author.id)
            pmCount = 1
        
        if message.content.startswith('!ban') and str(message.author.id) in dAdmins:
            if len(message.content) == 4 or len(message.content) == 5:
                client.send_message(message.channel, 'Who would you like to ban, ' + str(message.author)+'?')
            else:
                client.send_message(message.channel, message.content[5:]+' has been banned.')
        elif message.content.startswith('!ban') and str(message.author.id) not in dAdmins:
            client.send_message(message.channel, 'You are not an admin so you cannot access this command.')
        if message.content.startswith('!') == False:
            for t in twitchEmotes:
                if t in message.content:
                    client.send_file(message.channel, 'C:/DISCORD BOT/twitch emotes/'+t+'.jpg')
                    counts1 = 1
                    pmCount = 1
                    break  
            if counts1 == 1:
                counts1 = 0
            time.sleep(delayT)
        
        if message.content.startswith('!lightproc'):
            client.send_message(message.channel, 'Buckle up!')
            client.send_file(message.channel, 'Comphus.jpg')
            time.sleep(delayT)
            pmCount = 1
        if message.content.startswith('!retrievename'):
            client.send_message(message.channel, message.author)
            time.sleep(delayT)
            pmCount = 1
        """
        if message.content.startswith('!translate'):
            dTranslate = str(message.content)
            dTranslate = dTranslate.replace('!translate ', '')
            client.send_message(message.channel, 'https://translate.google.com/#auto/en/'+dTranslate)
            time.sleep(delayT)
            dTranslate = ''
            """
        if message.content.startswith('!hbddonkay'):
            client.send_message(message.channel,'Happy birthday <@90844964413505536>')
            client.send_file(message.channel,'birthday.jpg')
            newM = ''
            with codecs.open('cake.txt','r',"utf-8") as f:
                for i in f:
                    newM += i + '\n'
            client.send_message(message.channel, newM)
            pmCount = 1
        if message.content.startswith('!id'):
            newR = message.content[4:]
            if len(message.content.split()) == 1:
                    p = message.author.id
                    client.send_message(message.channel, p)
            else:
                if discord.utils.find(lambda m: m.name == newR, message.channel.server.members) == None:
                    client.send_message(message.channel, 'Person does not exist, or you tried to mention them')
                else:
                    p = discord.utils.find(lambda m: m.name == newR, message.channel.server.members).id
                    client.send_message(message.channel, p)
        if message.content.startswith('!avatar'):
            newR = message.content[8:]
            if len(message.content.split()) == 1:
                    p = message.author.avatar_url()
                    client.send_message(message.channel, p)
            else:
                if discord.utils.find(lambda m: m.name == newR, message.channel.server.members) == None:
                    client.send_message(message.channel, 'Person does not exist, or you tried to mention them')
                else:
                    p = discord.utils.find(lambda m: m.name == newR, message.channel.server.members).avatar_url()
                    client.send_message(message.channel, p)
            pmCount = 1
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
            client.send_message(message.channel, '```Name: {}\nID: {}\nDiscriminator: {}\nRoles: {}\nJoin Date: {}\nName Color: {}```'.format(p,p.id,p.discriminator,dRol,dJoin,str(dCol2)))
            pmCount = 1
        if message.content.startswith('!lawli'):
            client.send_message(message.channel,'(｡◕ ∀ ◕｡)')
            pmCount = 1
        if message.content.startswith('!domo'):
            client.send_message(message.channel,'\\\\|°▿▿▿▿°|/')
            pmCount = 1
        if message.content.startswith('おはよ'):
            client.send_message(message.channel, message.author.mention() + ' おはようございます~')
            pmCount = 1
        if message.content.startswith('!changeme') and len(message.content.split()) >= 3 and str(message.author.id) in '90886475373109248 90953831583617024 90869992689520640 90940396602953728 90847182772527104':
            # light pink FF69B4
            colorVal = message.content.split()[-1]
            roleName = message.content.replace('!changeme ', '')
            roleName = roleName.replace(' '+colorVal, '')
            print(roleName)
            print(colorVal)
            client.send_message(message.channel, 'None')
            if colorVal.startswith('0x') == False:
                client.send_message(message.channel, 'Make sure to add \'0x\' infront of your hex value!')
                counts1 = 1
            elif discord.utils.find(lambda r: r.name == str(roleName), message.channel.server.roles) == None:
                client.send_message(message.channel, 'Role name is invalid!')
                counts1 = 1
            elif counts1 == 0:
                client.edit_role(message.channel.server, discord.utils.find(lambda r: r.name == str(roleName), message.channel.server.roles), colour=discord.Colour(int(colorVal, 16)))
                client.send_message(message.channel, 'did it work')
            counts1 = 0
        elif message.content.startswith('!changeme') and len(message.content.split()) >= 3 and str(message.author.id) not in '90886475373109248 91347017103581184':
            client.send_message(message.channel, 'You do not have access to this command')
        if message.content.startswith('!me') and message.content.endswith('ep'):
            client.send_message(message.channel, 'me'+ 'e'*random.randint(0,40) +'ep')
            time.sleep(delayT)
            pmCount = 1
        if message.content.startswith('ayy lmao'):
            client.send_file(message.channel, 'AyyLmao.jpg')
            time.sleep(delayT)
            pmCount = 1
            
        if message.content.startswith('!debug') and str(message.author.id) == '90886475373109248':
            newM = message.content.replace('!debug ', '')
            
            try:
                if '`' in message.content:
                    newM = message.content.replace('`', '')
                    client.send_message(message.channel, str(eval(newM)))
                else:
                    client.send_message(message.channel, str(eval(newM)))
            except SyntaxError as e:
                client.send_message(message.channel, e)
            except ZeroDivisionError as e:
                client.send_message(message.channel, str(e)+' is not allowed. Evaluates to either ∞ or an indeterminate if 0/0')
            time.sleep(delayT)
            pmCount = 1
            
        if message.content.startswith('!turkeyme'):
            skeleR = random.randint(0,5)
            if skeleR <=4:
                client.send_message(message.channel, message.author.mention() + ' GOBBLE GOBBLE!')
                client.send_file(message.channel, 'turk'+str(skeleR)+'.jpg')
            elif skeleR <=5:
                client.send_message(message.channel, message.author.mention() + ' GIT GOBBLE GOBBLED!')
                client.send_file(message.channel, 'turk'+str(skeleR)+'.gif')
            else:
                client.send_message(message.channel, 'YOU\'VE BEEN SPOOKED TO DEATH\nhttps://www.youtube.com/watch?v=O8XfV8aPAyQ')
            time.sleep(delayT+2)
            pmCount = 1
            
        if message.content.startswith('!spookme'):
            skeleR = random.randint(0,39)
            if skeleR <=30:
                client.send_message(message.channel, message.author.mention() + ' YOU\'VE BEEN SPOOKED!')
                client.send_file(message.channel, 'skele'+str(skeleR)+'.jpg')
            elif skeleR <=38:
                client.send_message(message.channel, message.author.mention() + ' YOU\'VE BEEN SUPER SPOOKED!')
                client.send_file(message.channel, 'skele'+str(skeleR)+'.jpg')
            else:
                client.send_message(message.channel, 'YOU\'VE BEEN SPOOKED TO DEATH\nhttps://www.youtube.com/watch?v=O8XfV8aPAyQ')
            time.sleep(delayT+2)
            
        if 'random number' in str(message.content).lower():
            client.send_message(message.channel, str(random.randint(0,100))+'(0-100)')
            time.sleep(delayT)
            pmCount = 1
        if message.content.lower().startswith('!randomnumber'):
            randomN = str(message.content).split()
            client.send_message(message.channel, str(random.randint(int(randomN[1]),int(randomN[2])))+' ('+ randomN[1]+'-'+randomN[2]+')')
            time.sleep(delayT)
            pmCount = 1
        if message.content.startswith('<@106469383206883328>'):
            if 'who are you' == str(message.content).lower().replace('<@106469383206883328>'+ ' ', '') or 'who are you?' == str(message.content).lower().replace('<@106469383206883328>'+ ' ', ''):
                client.send_message(message.channel, 'I am a bot that runs on a community made python API(more info on that in bot-and-api channel) and programmed by Comphus to have functions for this discord server')
                counts1 = 1
            elif counts1 == 0:
                for word in qQuestion:
                    if word in str(message.content).lower():
                        client.send_message(message.channel, magicEight[random.randint(0,19)]+', ' +  message.author.mention())
                        counts1 = 1
                        break  
            if counts1 == 1:
                counts1 = 0
            elif 'hi' in message.content or 'Hi' in message.content or 'hello' in message.content or 'Hello' in message.content:
                client.send_message(message.channel, 'Hi! ' + message.author.mention())
            elif 'bye' in message.content or 'Bye' in message.content:
                client.send_message(message.channel, 'Bye-Bye! ' + message.author.mention())
            elif 'i love you' in message.content or 'I love you' in message.content or '<3' in message.content:
                client.send_message(message.channel, 'I love you too <3 ' + message.author.mention())
            elif 'thank' in message.content or 'Thanks' in message.content:
                client.send_message(message.channel, 'You\'re welcome! ' + message.author.mention())
            elif 'fuck you' in message.content or 'Fuck you' in message.content or 'Fuck u' in message.content or 'fuck u' in message.content or '( ° ͜ʖ͡°)╭∩╮' in message.content:
                client.send_message(message.channel, '( ° ͜ʖ͡°)╭∩╮ ' + message.author.mention())
            else:
                client.send_message(message.channel, 'what? ' + message.author.mention())
            time.sleep(delayT)
            pmCount = 1
        if 'fuck you bot' in message.content or 'fuck you dnbot' in message.content or 'fuck you discordbot' in message.content or 'fuck you dndiscordbot' in message.content or 'fuck you basedbot' in message.content:
            client.send_message(message.channel, message.author.mention() + ' ( ° ͜ʖ͡°)╭∩╮')
            time.sleep(delayT)
            pmCount = 1
        if 'thanks bot' in message.content or 'Thanks bot' in message.content or 'Thank you bot' in message.content or 'thank you bot' in message.content or 'thank u' in message.content or 'Thank u' in message.content:
            client.send_message(message.channel, message.author.mention() + ' You\'re welcome!')
            time.sleep(delayT)
            pmCount = 1
            
        """
        if message.content.startswith('!ascend'):
            client.send_message(message.channel, 'AHHHHHHHHH. Level: ' + str(gAscend))
            gAscend += 1
            time.sleep(delayT)
        if message.content.startswith('!descend'):
            client.send_message(message.channel, 'AHHHHHHHHH. Level: ' + str(gAscend))
            gAscend -= 1
            time.sleep(delayT)
        """
        if str(message.channel.server.id) == '106293726271246336':
            with io.open('chatLogs.txt','a',encoding='utf-8') as f:
                logT = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                logM = (str(message.author)+'('+str(message.author.id)+') '+ logT +': '+str(message.content)+'\n')
                f.write(logM)
            if message.content.startswith('!chatlogs') and str(message.author.id) in dAdmins and str(message.channel.id) == '106560613794197504':
                client.send_file(message.channel, 'chatLogs.txt')
        if message.channel.is_private == True and str(message.author.id) != '106469383206883328':
            
            if message.content.startswith('!info'):
                client.send_message(message.channel, """Hello, I am BASEDBOT! I see you have PMed me and used the !info command, so I will tell you stuff about me!
I am a bot created by Comphus(light damage guy/kdn guy) with the purpose of making life in discord easier and more fun for others in the servers I join(no I do not automatically join servers with a link)
The main server I was created for is the Dragon Nest community discord, if you play dragon nest in NA, any other version, or hell just want to join cause you have friends here, then go for it! Just dont break the rules!
If you wish to know what commands I have, you can do `!commands` to see(note, there are a number of commands that are not on that list for privacy purposes). All of these commands should work in PMs.
You may also ask me a question(make sure to end it with a '?' so I know its a question, has to be at least 3 characters long) and I will give you a magic eight ball reponse.
If you wish to join, there should be a link on reddit and the DNNA forums somewhere!
        """)
                client.send_file(message.channel, 'Welcome.jpg')
            elif '?' in message.content and len(message.content) > 2:
                client.send_message(message.channel, magicEight[random.randint(0,19)])
            elif 'help' in message.content.lower():
                client.send_message(message.channel, 'If you need help, do !info')
            elif 'join' in message.content.lower():
                client.send_message(message.channel, 'I do not join servers via command, if you want me to join your server, contact my creator, Comphus, and he will decide if I can be in your server. He is usually in the Dragon Nest community discord, if you want to join it, find the link on the discord reddit in public servers!')
            #elif len(message.content) > 0 and pmCount == 0:
            #    client.send_message(message.channel, 'Hello! If you wish to know more about me, type in !info')
            
        pmCount = 0

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
