import discord
import asyncio

player = {}
musicQue = {}
voice = {}
sToken = {}
class musicbot:
	"""
	makes music
	"""

	def __init__(self, bot):
		self.bot = bot
		self.musicControls = ["next", "skip", "list", "song","pause", "resume", "help"]

	async def playmusic(self, message, sid):
		if (len(message.content.split()) == 2 or 'volume' in message.content) == False:
			await self.bot.send_message(message.channel, 'You must have a link to show after !yt. It can be almost anything, youtube, soundcloud, even pornhub!')
			return
		if 'help' in message.content:
			await self.bot.send_message(message.channel, 'How to make the !yt function work, type in \'!yt \', then whatever url you want afterwards to make it play its audio, will not play from ALL links.\n__Commands you can put in after !yt for !yt are:__\n**next/skip** - goes to the next song, if there isnt one then the bot leaves\n**list** - a list of songs in queue\n**song** - current song playing\n**pause/resume** - pauses or resumes the song\n**stop** - stops the music bot and removes it from the channel, use this incase it breaks, or to end the session\n**volume** - can change volume of bot to either 0 or 200%, ex: !yt volume 50\n**help** - pulls up this text')
			return
		ctrC = message.content.lower().split()[1]
		try:
			if sid not in voice:
				voice[sid] = await self.bot.join_voice_channel(message.author.voice_channel)
				musicQue[sid] = []
				player[sid] = None
				sToken[sid] = False
		except:
			await self.bot.send_message(message.channel, "You are not in a voice channel, please join a voice channel in order to play music.")
			return
		try:
			if voice[sid] == None:
				voice[sid] = await self.bot.join_voice_channel(message.author.voice_channel)
				musicQue[sid] = []
				player[sid] = None
				sToken[sid] = False
		except:
			await self.bot.send_message(message.channel, "You are not in a voice channel, please join a voice channel in order to play music.")
			return
		if 'stop' in message.content:
			if voice[sid].is_connected():
				player[sid] = None
				await voice[sid].disconnect()
				musicQue[sid] = []
				voice[sid] = None
				sToken[sid] = False
				print('Used !stop in:' + sid)
				return
		if ('next' in message.content or 'skip' in message.content) and player[sid] != None:
			if voice[sid].is_connected():
				player[sid].stop()
				if len(musicQue[sid]) == 0:
					await voice[sid].disconnect()
					musicQue[sid] = []
				return
		if 'pause' in message.content and player[sid] != None:
			if voice[sid].is_connected():
				player[sid].pause()
				return
		if 'resume' in message.content and player[sid] != None:
			if voice[sid].is_connected():
				player[sid].resume()
				return
		if 'volume' in message.content and player[sid] != None:
			if type(int(message.content[-1])) == type(5):
				vol = int(message.content.split()[-1])
				if vol > 200 or vol < 0:
					await self.bot.send_message(message.channel, 'volume number must be between 0 and 200')
					return
				elif vol <= 200 and vol >= 0:
					v = (vol/100.0)
					player[sid].volume = v
					return
			elif type(int(message.content[-1])) != type(5):
				await self.bot.send_message(message.channel, 'that is not a number')
			return
		if 'list' in message.content and player[sid] != None and len(musicQue[sid]) >0:
			returnS = ''
			for i in musicQue[sid]:
				if i not in self.musicControls:
					returnS += (i+'\n')
			await self.bot.send_message(message.channel, 'Current list of music in queue\n\n'+returnS)
			returnS = ''
		if 'song' in message.content and player[sid] != None and len(musicQue[sid]) >0:
			await self.bot.send_message(message.channel, 'Current song playing: **'+ player[sid].title+'**')
		async def runmusic(message, sid, sToken):
			async def playmusicque(queurl):
				try:
					if player[sid] != None:
						player[sid].stop()
						player[sid] = await voice[sid].create_ytdl_player(queurl)
						player[sid].start()
						musicQue[sid].pop(0)
						await self.bot.send_message(message.channel, '**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(player[sid].title, player[sid].views, player[sid].likes, player[sid].dislikes))
						return
					else:
						player[sid] = await voice[sid].create_ytdl_player(queurl)
						player[sid].start()
						musicQue[sid].pop(0)
						await self.bot.send_message(message.channel, '**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(player[sid].title, player[sid].views, player[sid].likes, player[sid].dislikes))
						return
				except Exception as e:
					musicQue[sid].pop(0)
					await self.bot.send_message(message.channel, e)
					if len(musicQue[sid]) == 0:
						await self.bot.send_message(message.channel, "No more songs in queue")
						player[sid] = None
						await voice[sid].disconnect()
						voice[sid] = None
						sToken = False
					return
			if ctrC not in self.musicControls:
				endurl = message.content.split()[1]
				musicQue[sid].append(endurl)
				#the loop
				if sToken[sid] == False:
					sToken[sid] = True
					print('started in '+ sid)
					try:
						print('server name is: '+ message.server.name)
					except:
						pass
					while len(musicQue[sid]) >= 0:
						if player[sid] == None:
							if len(musicQue[sid]) == 1:
								await playmusicque(musicQue[sid][0])
						await asyncio.sleep(2)
						try:
							if player[sid].is_done():
								if len(musicQue[sid]) == 0:
									await self.bot.send_message(message.channel, "No more songs in queue")
									player[sid] = None
									await voice[sid].disconnect()
									voice[sid] = None
									sToken = False
									print('ended in '+sid)
								elif len(musicQue[sid]) > 0:
									await playmusicque(musicQue[sid][0])
						except:
							pass
						try:
							if len(musicQue[sid]) == 0 and player[sid].is_done():
								break
						except:
							pass
						if len(musicQue[sid]) == 0 and player[sid] == None:
							break
		await runmusic(message, sid, sToken)
