import requests
import json
import asyncio
import random
import time
from discord.ext import commands
import discord

tPlayers = {}
tStop = {}
TriviaQuestions = {}
class overwatch:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True)
	async def ow(self, ctx):
		await self.owcheck(ctx.message)
		
	async def owcheck(self, message):
		if '#' not in message.content[4:]:
			await self.bot.send_message(message.channel, 'You need a # between your name and your number.')
			return
		elif '#' in message.content[4:]:
			newestM = message.content[4:].replace('#', '-')
			newerM = 'https://masteroverwatch.com/profile/pc/us/'+newestM
			r = requests.get(newerM)
			from bs4 import BeautifulSoup
			soup = BeautifulSoup(r.text, 'html.parser')
			test = soup.find_all(attrs={"class":"error"})
			if len(test) > 0:
				await self.bot.send_message(message.channel, newerM +'\nInvalid player name.(you might have to visit the site first so their database can save you)')
				return
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
				await self.bot.send_message(message.channel, "{}\n```xl\n{}          Level: {}\nRank: {}          Win Rate: {}          Win-Loss: {}```\n**__TOP 3 HEROES__**\n{}\n{}\n{}".format(newerM,bnet,plevel,rank,wrate,totg,h1,h2,h3))
				return

	def tCheck(self, sid):
		try:
			return tStop[sid]
		except:
			return False

	async def trivia(self, message, sid):
		with open("C:/DISCORD BOT/Games/triviacontent.json") as j:
			QuizResponses = json.load(j)
		tPlayers[sid] = {}
		tStop[sid] = True
		await self.bot.send_message(message.channel, "You have started the Overwatch Trivia! These questions will start up in 5 seconds! Use |stop to stop the trivia and |points to see points!")
		TriviaQuestions[sid] = QuizResponses['overwatch']
		print(len(TriviaQuestions[sid]))
		print(len(QuizResponses['overwatch']))
		await asyncio.sleep(2)
		while len(TriviaQuestions[sid]) > 0 and tStop[sid]:
			await asyncio.sleep(3)
			TriviaQuestion = random.choice(list(TriviaQuestions[sid].keys()))
			await self.bot.send_message(message.channel, "**The question is:**\n{}".format(TriviaQuestion))
			answer = TriviaQuestions[sid][TriviaQuestion]
			end_time = time.time() + 15
			while True:
				time_remaining = end_time - time.time()
				if time_remaining <= 0:
					await self.bot.send_message(message.channel, '**Sorry, you took too long! The answer was:**\n```xl\n{}```'.format(answer))
					del TriviaQuestions[sid][TriviaQuestion]
					break
				guess = await self.bot.wait_for_message(timeout = time_remaining)
				if guess and answer in guess.content.lower():
					await self.bot.send_message(message.channel, '**Congratulations** {}! **You\'ve won!**'.format(guess.author.mention))
					if guess.author.mention not in tPlayers[sid]:
						tPlayers[sid][guess.author.mention] = 1
					elif guess.author.mention in tPlayers[sid]:
						tPlayers[sid][guess.author.mention] += 1
					del TriviaQuestions[sid][TriviaQuestion]
					break
			print(len(TriviaQuestions[sid]))
		if len(TriviaQuestions[sid]) == 0 and message.channel.id != '106293726271246336':
			await self.bot.send_message(message.channel, "There are no more questions left!")
			tStop[sid] = False
			a = '**RESULTS**\n'
			for i in tPlayers[sid]:
				a+= '{} with {} points\n'.format(i,tPlayers[sid][i])
			await self.bot.send_message(message.channel, a)
			tPlayers[sid] = {}
			return

	async def stopTrivia(self, message, sid):
		if tStop[sid] != True:
			await self.bot.send_message(message.channel, 'Trivia hasnt started yet!')
			return
		if tStop[sid]:
			await self.bot.send_message(message.channel, "Trivia has stopped! The last question will continue!")
			tStop[sid] = False
			a = '**RESULTS**\n'
			for i in tPlayers[sid]:
				a+= "{} with {} points\n".format(i,tPlayers[sid][i])
			await self.bot.send_message(message.channel, a)
			tPlayers[sid] = {}
			#TriviaQuestions[sid] = {}
		return

	async def points(self, message, sid):
		a = '**RESULTS**\n'
		for i in tPlayers[sid]:
			a+= '{} with {} points\n'.format(i,tPlayers[sid][i])
		await self.bot.send_message(message.channel, a)
	
	async def on_message(self, message):
		if self.bot.user == message.author or message.channel.id == '168949939118800896' or message.author.id in '128044950024617984':
			return
		if message.content.startswith('|trivia') and self.tCheck(message.server.id) != True and message.channel.id != '106293726271246336':
			await self.trivia(message, message.server.id)
		elif message.content.startswith('|stop') and message.channel.id != '106293726271246336':
			await self.stopTrivia(message, message.server.id)
		elif message.content.startswith('|points') and message.channel.id != '106293726271246336':
			await self.points(message, message.server.id)

def setup(bot):
	bot.add_cog(overwatch(bot))
