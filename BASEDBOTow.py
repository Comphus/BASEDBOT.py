import requests

def ow(newM):
	if '#' not in newM:
		return 'You need a # between your name and your number.'
	elif '#' in newM:
		newestM = newM.replace('#', '-')
		newerM = 'https://masteroverwatch.com/profile/pc/us/'+newestM
		r = requests.get(newerM)
		from bs4 import BeautifulSoup
		soup = BeautifulSoup(r.text, 'html.parser')
		test = soup.find_all(attrs={"class":"error"})
		if len(test) > 0:
			return newerM +'\nInvalid player name.(you might have to visit the site first so their database can save you)'
		elif len(test) == 0:
			#print(soup.find_all('body')[0].find_all(attrs={"class":"heroes-list"}))
			heroes = soup.find_all(attrs={"class":"summary-list"})
			bnet = soup.find_all(attrs={"class":"header-box"})[0].h1.text.split()[0]
			plevel = soup.find_all(attrs={"class":"header-box"})[0].find_all(attrs={"class":"header-avatar"})[0].span.string
			try:
				rank = soup.find_all(attrs={"class":"header-stats"})[0].find_all(attrs={"class":"header-stat"})[0].text.splitlines()[3].split()[0]
			except:
				rank = 'No Rank'
			#print(soup.find_all(attrs={"class":"header-stats"})[0].find_all(attrs={"class":"header-stat"})[0].text.splitlines()[3].split()[0])
			totg = soup.find_all(attrs={"class":"header-stats"})[0].find_all(attrs={"class":"header-stat"})[2].strong.text.split()[0]
			wrate = soup.find_all(attrs={"class":"header-stats"})[0].find_all(attrs={"class":"header-stat"})[3].strong.string.split()[0]
			#print(heroes[0].find_all(attrs={"class":"summary-icon col-xs-5"})[0].strong.span.string)
			#print(heroes[0].find_all(attrs={"class":"summary-stats-kda"})[0].text)
			#print(heroes[0].find_all(attrs={"class":"summary-winrate col-xs-3"})[0].strong.text)
			hero1 = [heroes[0].find_all(attrs={"class":"summary-icon col-xs-5"})[0].strong.span.string, heroes[0].find_all(attrs={"class":"summary-stats-kda"})[0].text, heroes[0].find_all(attrs={"class":"summary-winrate col-xs-3"})[0].strong.text, soup.find_all(attrs={"class":"card-primary-stats"})[0].find_all(attrs={"class":"stat-row stat-playtime"})[0].text]
			try:
				hero2 = [heroes[0].find_all(attrs={"class":"summary-icon col-xs-5"})[1].strong.span.string, heroes[0].find_all(attrs={"class":"summary-stats-kda"})[1].text, heroes[0].find_all(attrs={"class":"summary-winrate col-xs-3"})[1].strong.text, soup.find_all(attrs={"class":"card-primary-stats"})[2].find_all(attrs={"class":"stat-row stat-playtime"})[0].text]
			except:
				hero2 = ["None","None","None","None"]
			try:
				hero3 = [heroes[0].find_all(attrs={"class":"summary-icon col-xs-5"})[2].strong.span.string, heroes[0].find_all(attrs={"class":"summary-stats-kda"})[2].text, heroes[0].find_all(attrs={"class":"summary-winrate col-xs-3"})[2].strong.text,soup.find_all(attrs={"class":"card-primary-stats"})[1].find_all(attrs={"class":"stat-row stat-playtime"})[0].text]
			except:
				hero3 = ["None","None","None","None"]
			h1 = '**{}:** {}               W/L% = {}          Time Played: {}'.format(hero1[0], hero1[1], hero1[2], hero1[3])
			h2 = '**{}:** {}               W/L% = {}          Time Played: {}'.format(hero2[0], hero2[1], hero2[2], hero3[3])
			h3 = '**{}:** {}               W/L% = {}          Time Played: {}'.format(hero3[0], hero3[1], hero3[2], hero2[3])
			return "{}\n```xl\n{}          Level: {}\nRank: {}          Win Rate: {}          Win-Loss: {}```\n**__TOP 3 HEROES__**\n{}\n{}\n{}".format(newerM,bnet,plevel,rank,wrate,totg,h1,h2,h3)
