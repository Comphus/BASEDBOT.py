import requests
import json
import random
import re

with open("malinfo.json") as j:
	malinfo = json.load(j)

def defines(message):
	if len(message.content.split()) == 1:
		return 'need something to define'
	words = message.content[8:]
	r = requests.get('http://api.urbandictionary.com/v0/define?term=' + words)
	tData = r.json()
	if r.status_code == 200:
		try:
			i = random.randint(0, len(tData['list'])-1)
			dWord = tData['list'][i]['word']
			dDef = tData['list'][i]['definition']
			dEx = tData['list'][i]['example']
			return "__Word__: {}\n__**Definition**__\n{}".format(dWord,dDef,dEx)
		except:
			return 'Word is not defined'
	else:
		return 'something went wrong :('

def mal(message):
	if message.content.lower().split()[0] == '!mal' and len(message.content.split()) == 1:
		return 'https://myanimelist.net/'
	import xml.etree.ElementTree as ET
	anime = message.content.lower()[5:]
	r = requests.get('http://myanimelist.net/api/anime/search.xml?q=' + anime, auth=(malinfo['maluser'], malinfo['malpassword']))
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
		return "**Name: **{}\n**Eng Name: **{}\n**Status: **{}\n**Air Date: **{}\n**Episodes: **{}\n**Score: **{}\n**Description: **{}\n**Link: **{}".format(aJp,aName,aStat,aDate,aEp,aScore,aDesc,aUrl)
	elif r.status_code == 204:
		return "I couldnt find an anime with that name in MyAnimeList"
	else:
		return "MyAnimeList is down, NOOOOOOOO :("

def checktwitch(message):
	if len(message.content.split()) != 2:
		return 'The format of !checktwitch is `!checktwitch (channelname).`'
	tChan = message.content.split()[-1].lower()
	r = requests.get('https://api.twitch.tv/kraken/streams/{}/?&client_id=(your client id)'.format(tChan))
	if r.status_code == 200:
		tData = r.json()
		if tData['stream'] == None:
			return tChan+'\'s channel is currently offline!'
		else:
			return tChan+'\'s channel is currently online!\n'+tChan+' is currently playing {} with {} viewers!\n{}'.format(tData['stream']['game'], str(tData['stream']['viewers']), 'http://www.twitch.tv/'+tChan)
	elif r.status_code == 404:
		return 'This channel does not exist.'
	elif r.status_code == 422:
		return 'Channel ' + tChan + ' is a justin.tv channel and doesnt work on twitch or is banned!'
