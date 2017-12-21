import asyncio
import aiohttp
import discord
from cogs.utils import checks
from discord.ext import commands
import json
from bs4 import BeautifulSoup
import re


class background_tasked():
	def __init__(self, bot):
		self.bot = bot
		self.bg_task = self.bot.loop.create_task(self.feedtask())
		self.colors = {
				"update":0x40AA01,
				"maint.":0xda99d9,
				"event":0xffb816,
				"notice":0x12A1F3
			}


	def __unload(self):
		self.bg_task.cancel()

	async def feedtask(self):
		print("hi")
		await self.bot.wait_until_ready()
		with open("C:/DISCORD BOT/DragonNest/dnfeed.json") as j:
			feedinfo = json.load(j)
		current = feedinfo["num"]
		currenttit = feedinfo["tit"]
		ch = self.bot.get_channel(106293726271246336)#currently DNCD exclusive
		if ch is None:
			return
		link = "http://us.dragonnest.com/news/notice/all"
		print("it turned on")
		while not self.bot.is_closed():
			async with aiohttp.ClientSession() as session:
				async with session.get(link) as r:
					if r.status == 200:
						t = await r.text()
						soup = BeautifulSoup(t, 'html.parser')
						insides = soup.find_all("tbody")[0]
						currentnum = int(insides.find_all(attrs={"class":"num"})[0].string)
						tit = insides.find_all(attrs={"class":"subject"})[0].span.string
						if int(currentnum) > current or (tit.lower() != currenttit and int(currentnum) >= current):
							cat = insides.find_all(attrs={"class":"category"})[0].span.string
							current = int(currentnum)
							currenttit = tit.lower()
							feedinfo["num"] = current
							feedinfo["tit"] = currenttit
							with open("C:/DISCORD BOT/DragonNest/dnfeed.json", 'w') as file:
								json.dump(feedinfo, file, indent = 4)
							newURL = "{}/{}".format(link,current)
							async with aiohttp.ClientSession() as sess:
								async with sess.get(newURL) as rr:
									news = await rr.text()
							soup2 = BeautifulSoup(news, 'html.parser')
							alltext = soup2.find_all("div", class_="cont")[0].find_all("p")#.strip('<p>').strip('</p>').strip('<span style="color:#000000;">').strip('<span>').strip("&nbsp;")
							finaltext = ""
							for i in range(5):
								try:
									cleanr = re.compile('<.*?>')
									cleantext = re.sub(cleanr, '', str(alltext[i]).replace("<strong>", "**").replace("</strong>", "**"))
									finaltext += (cleantext + "\n") 
								except:
									pass
							finaltext += "...\nRead more at {}".format(newURL)
							col = self.colors[cat.lower()]
							embed = discord.Embed()
							embed.set_author(name=cat,icon_url="http://i.imgur.com/Kj9B0O9.png")
							embed.color = col
							embed.title = tit
							embed.url = newURL
							embed.description = finaltext
							embed.set_footer(text='Dragon Nest Live Feed', icon_url='http://i.imgur.com/0zURV1B.png')
							await ch.send("<@&292111551626870784>",embed=embed)
			await asyncio.sleep(60)


def setup(bot):
	bot.add_cog(background_tasked(bot))