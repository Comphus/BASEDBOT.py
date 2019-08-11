import aiohttp
import json
import asyncio
import random
import time
from bs4 import BeautifulSoup
from discord.ext import commands
import discord
from .utils import checks

tPlayers = {}
tStop = {}
TriviaQuestions = {}
class overwatch(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		

	async def ranks(self, r, e):
		print(r)
		if r < 1500:
			e.set_thumbnail(url="http://i.imgur.com/2T4pqKo.png")
			e.color = 6700326
		elif r < 2000:
			e.set_thumbnail(url="http://i.imgur.com/93ZBbro.png")
			e.color = 12632256
		elif r < 2500:
			e.set_thumbnail(url="http://i.imgur.com/smnzdD0.png")
			e.color = 16766720
		elif r < 3000:
			e.set_thumbnail(url="http://i.imgur.com/DgBmFGJ.png")
			e.color = 15066338
		elif r < 3500:
			e.set_thumbnail(url="http://i.imgur.com/aqoNZrp.png")
			e.color = 9414120
		elif r < 4000:
			e.set_thumbnail(url="http://i.imgur.com/32IkIY9.png")
			e.color = 16768819
		else:
			e.set_thumbnail(url="http://i.imgur.com/s8q2Fnp.png")
			e.color = 16770919
		return e

	@commands.command()
	@checks.not_lounge()
	async def ow(self, ctx, *, m : str = None):
		if m is None:
			await ctx.send("need your battletag to find your Overwatch profile.")
			return
		elif '#' not in m:
			await ctx.send('You need a # between your name and your number.')
			return
		else:
			newestM = m.replace('#', '-')
			newerM = 'https://www.overbuff.com/players/pc/'+newestM
			async with aiohttp.ClientSession() as session:
				async with session.get(newerM) as r:
					s = await r.text()
				if True:
					soup = BeautifulSoup(s, 'html.parser')
					test = soup.find_all(attrs={"class":"layout-error"})
					if len(test) > 0:
						await ctx.send(newerM +'\nInvalid player name.(you might have to visit the site first so their database can save you)')
						return
					elif len(test) == 0:
						bnet = soup.find_all(attrs={"class":"layout-header-primary"})[0].h1.text.replace('"', "")
						picon = soup.find_all(attrs={"class":"image-with-corner"})[0].img['src']
						plevel = soup.find_all(attrs={"class":"corner corner-text"})[0].text
						try:
							rank = soup.find_all(attrs={"class":"color-stat-rating"})[0].string
						except:
							rank = 'No Rank'
						try:
							skrank = soup.find_all(attrs={"rel":"tooltip"})[0].string
						except:
							skrank = "No Skill Rank"

						if rank != "No Rank":
							newerM = 'https://www.overbuff.com/players/pc/'+newestM+'?mode=competitive'
							async with aiohttp.ClientSession() as session:
								async with session.get(newerM) as r:
									s = await r.text()
							soup = BeautifulSoup(s, 'html.parser')
							print("it did comp")

						win = soup.find_all(attrs={"class":"color-stat-win"})[0].string
						loss = soup.find_all(attrs={"class":"color-stat-loss"})[0].string
						wl = "{} - {}".format(win,loss)
						
						heroes = soup.find_all(attrs={"class":"player-heroes"})
						try:
							hero1 = [heroes[0].find_all(attrs={"class":"name"})[0].a.string, 
							heroes[0].find_all(attrs={"class":"group special"})[0].find_all(attrs={"rel":"tooltip"})[0].string, 
							"{} - {}".format(heroes[0].find_all(attrs={"class":"color-stat-win"})[0].string,
								heroes[0].find_all(attrs={"class":"color-stat-loss"})[0].string), 
							heroes[0].find_all(attrs={"class":"stat padded"})[0].find_all(attrs={"class":"value"})[0].text,
							"https://www.overbuff.com{}".format(heroes[0].find_all(attrs={"class":"image-with-corner"})[0].img['src'])]
						except:
							hero1 = ["None","None","None","None"]
						try:
							hero2 = [heroes[0].find_all(attrs={"class":"name"})[1].a.text, 
						heroes[0].find_all(attrs={"class":"group special"})[2].find_all(attrs={"rel":"tooltip"})[0].text, 
						"{} - {}".format(heroes[0].find_all(attrs={"class":"color-stat-win"})[1].string,
							heroes[0].find_all(attrs={"class":"color-stat-loss"})[1].string), 
						heroes[0].find_all(attrs={"class":"stat padded"})[3].find_all(attrs={"class":"value"})[0].text,
						"https://www.overbuff.com{}".format(heroes[0].find_all(attrs={"class":"image-with-corner"})[1].img['src'])]
						except:
							hero2 = ["None","None","None","None"]
						try:
							hero3 = [heroes[0].find_all(attrs={"class":"name"})[2].a.text, 
						heroes[0].find_all(attrs={"class":"group special"})[4].find_all(attrs={"rel":"tooltip"})[0].text, 
						"{} - {}".format(heroes[0].find_all(attrs={"class":"color-stat-win"})[2].string,
							heroes[0].find_all(attrs={"class":"color-stat-loss"})[2].string), 
						heroes[0].find_all(attrs={"class":"stat padded"})[6].find_all(attrs={"class":"value"})[0].text,
						"https://www.overbuff.com{}".format(heroes[0].find_all(attrs={"class":"image-with-corner"})[2].img['src'])]
						except:
							hero3 = ["None","None","None","None"]
						totalheroes = [hero1, hero2, hero3]
						embed = discord.Embed()
						embed.set_author(name=bnet,icon_url=picon)
						embed.title = bnet
						embed.url = newerM
						embed.add_field(name="__General Info__",value="**Level:** {}\n**Rank:** {}\n**Skill Rank:** {}\n**Win/Loss:** {}".format(plevel,rank,skrank,wl), inline=False)
						for i in totalheroes:
							if i[0] != "None":
								embed.add_field(name="__{}__".format(i[0]),value="**Rank:** {}\n**Win/Loss:** {}\n**Time Played:** {}".format(i[1],i[2],i[3]))
						if rank != "No Rank":
							embed.description = "__**COMPETITIVE STATS**__"
							await self.ranks(int(rank), embed)
						else:
							embed.description = "__**QUICK PLAY STATS**__"
							embed.set_thumbnail(url=picon)
							embed.color = 6697881
						await ctx.send(embed=embed)
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
		await message.channel.send("You have started the Overwatch Trivia! These questions will start up in 5 seconds! Use |stop to stop the trivia and |points to see points!")
		TriviaQuestions[sid] = QuizResponses['overwatch']
		print(len(TriviaQuestions[sid]))
		print(len(QuizResponses['overwatch']))
		await asyncio.sleep(2)
		while len(TriviaQuestions[sid]) > 0 and tStop[sid]:
			await asyncio.sleep(3)
			TriviaQuestion = random.choice(list(TriviaQuestions[sid].keys()))
			await message.channel.send("**The question is:**\n{}".format(TriviaQuestion))
			answer = TriviaQuestions[sid][TriviaQuestion]
			try:
				guess = await self.bot.wait_for("message",timeout = 15)
			except asyncio.TimeoutError:
				await message.channel.send('**Sorry, you took too long! The answer was:**\n```xl\n{}```'.format(answer))
				del TriviaQuestions[sid][TriviaQuestion]
				break
			else:
				print("hi")
				if guess and answer in guess.content.lower():
					await message.channel.send('**Congratulations** {}! **You\'ve won!**'.format(guess.author.mention))
					if guess.author.mention not in tPlayers[sid]:
						tPlayers[sid][guess.author.mention] = 1
					elif guess.author.mention in tPlayers[sid]:
						tPlayers[sid][guess.author.mention] += 1
					del TriviaQuestions[sid][TriviaQuestion]
					break
			print(len(TriviaQuestions[sid]))
		if len(TriviaQuestions[sid]) == 0 and message.channel.id != 106293726271246336:
			await message.channel.send("There are no more questions left!")
			tStop[sid] = False
			a = '**RESULTS**\n'
			for i in tPlayers[sid]:
				a+= '{} with {} points\n'.format(i,tPlayers[sid][i])
			await message.channel.send(a)
			tPlayers[sid] = {}
			return

	async def stopTrivia(self, message, sid):
		if tStop[sid] != True:
			await message.channel.send('Trivia hasnt started yet!')
			return
		if tStop[sid]:
			await message.channel.send("Trivia has stopped! The last question will continue!")
			tStop[sid] = False
			a = '**RESULTS**\n'
			for i in tPlayers[sid]:
				a+= "{} with {} points\n".format(i,tPlayers[sid][i])
			await message.channel.send(a)
			tPlayers[sid] = {}
			#TriviaQuestions[sid] = {}
		return

	async def points(self, message, sid):
		a = '**RESULTS**\n'
		for i in tPlayers[sid]:
			a+= '{} with {} points\n'.format(i,tPlayers[sid][i])
		await message.channel.send(a)
	
	@commands.Cog.listener()
	async def on_message(self, message):
		if self.bot.user == message.author or message.channel.id == 168949939118800896 or message.author.id == 128044950024617984:
			return
		if message.content.startswith('|trivia') and self.tCheck(message.guild.id) != True and message.channel.id != 106293726271246336:
			await message.channel.send("Overwatch trivia is currently down for a major overhaul.(basically !quiz template)")
			#await self.trivia(message, message.guild.id)
		#elif message.content.startswith('|stop') and message.channel.id != 106293726271246336:
			#await self.stopTrivia(message, message.guild.id)
		#elif message.content.startswith('|points') and message.channel.id != 106293726271246336:
			#await self.points(message, message.guild.id)

def setup(bot):
	bot.add_cog(overwatch(bot))