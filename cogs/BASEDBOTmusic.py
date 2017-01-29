import discord
from discord.ext import commands
import asyncio

player = {}
musicQue = {}
voice = {}
sToken = {}


def player_exists():
	def predicate(ctx):
		try:
			return player[ctx.message.server.id] is not None
		except Exception:
			return False
	return commands.check(predicate)

class musicbot:
	"""
	makes music
	"""

	def __init__(self, bot):
		self.bot = bot

	async def playmusicque(self, queurl, sid, message):
		try:
			if player[sid] != None:
				player[sid].stop()
				player[sid] = await voice[sid].create_ytdl_player(queurl)
				player[sid].start()
				musicQue[sid].pop(0)
				await self.bot.say('**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(player[sid].title, player[sid].views, player[sid].likes, player[sid].dislikes))
				return
			else:
				player[sid] = await voice[sid].create_ytdl_player(queurl)
				player[sid].start()
				musicQue[sid].pop(0)
				await self.bot.say('**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(player[sid].title, player[sid].views, player[sid].likes, player[sid].dislikes))
				return
		except Exception as e:
			musicQue[sid].pop(0)
			await self.bot.send_message(message.channel, str(e))
			if len(musicQue[sid]) == 0:
				await self.bot.send_message(message.channel, "No more songs in queue")
				await self.complete_stop(sid)
			return

	async def runmusic(self, message, sid, sToken):
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
						await self.playmusicque(musicQue[sid][0],sid, message)
				await asyncio.sleep(2)
				try:
					if player[sid].is_done():
						if len(musicQue[sid]) == 0:
							await self.bot.say("No more songs in queue")
							await self.complete_stop(sid)
							print('ended in '+sid)
						elif len(musicQue[sid]) > 0:
							await self.playmusicque(musicQue[sid][0], sid, message)
				except:
					pass
				try:
					if len(musicQue[sid]) == 0 and player[sid].is_done():
						break
				except:
					pass
				if len(musicQue[sid]) == 0 and player[sid] == None:
					break

	async def playmusic(self, message, sid):
		if sid not in voice or voice[sid] == None:
			await self.complete_stop(sid)#just in case i happened to restart bot manually and its still in voice
			voice[sid] = await self.bot.join_voice_channel(message.author.voice_channel)
			musicQue[sid] = []
			player[sid] = None
			sToken[sid] = False

		await self.runmusic(message, sid, sToken)

	@commands.group(pass_context=True, invoke_without_command=False)#main command
	async def yt(self, ctx):
		if ctx.message.author.voice.voice_channel is None:
			await self.bot.say("You are not in a voice channel, please join a voice channel in order to play music.")
			return
		elif ctx.invoked_subcommand is not None:
			return
		elif len(ctx.message.content.split()) != 2:
			await self.bot.say('You must have a link to show after !yt. It can be almost anything, youtube, soundcloud, even pornhub!')
			return

		await self.playmusic(ctx.message, ctx.message.server.id)

	async def complete_stop(self, sid):
		try:
			await voice[sid].disconnect()
		except Exception:
			pass
		player[sid] = None
		musicQue[sid] = []
		voice[sid] = None
		sToken[sid] = False

	@yt.command()#all sub commands from here and below
	async def help(self):
		await self.bot.say('How to make the !yt function work, type in \'!yt \', then whatever url you want afterwards to make it play its audio, will not play from ALL links.\n__Commands you can put in after !yt for !yt are:__\n**next/skip** - goes to the next song, if there isnt one then the bot leaves\n**list** - a list of songs in queue\n**song** - current song playing\n**pause/resume** - pauses or resumes the song\n**stop** - stops the music bot and removes it from the channel, use this incase it breaks, or to end the session\n**volume** - can change volume of bot to either 0 or 200%, ex: !yt volume 50\n**help** - pulls up this text')

	@yt.command(pass_context=True)
	async def stop(self, ctx):
		await self.complete_stop(ctx.message.server.id)
		print('Used !stop in: ' + ctx.message.server.id)

	@yt.command(aliases=['next'], pass_context=True)
	@player_exists()
	async def skip(self, ctx):
		sid = ctx.message.server.id
		if voice[sid].is_connected():
			player[sid].stop()
			if len(musicQue[sid]) == 0:
				await voice[sid].disconnect()
				musicQue[sid] = []

	@yt.command(pass_context=True)
	@player_exists()
	async def pause(self, ctx):
		sid = ctx.message.server.id
		if voice[sid].is_connected():
				player[sid].pause()

	@yt.command(pass_context=True)
	@player_exists()
	async def resume(self, ctx):
		sid = ctx.message.server.id
		if voice[sid].is_connected():
				player[sid].resume()

	@yt.command(pass_context=True, aliases=['vol'])
	@player_exists()
	async def volume(self, ctx, vol : int = None):
		sid = ctx.message.server.id
		if vol is None or vol > 200 or vol < 0:
			await self.bot.say('volume number must be between 0 and 200')
		else:
			v = (vol/100.0)
			player[sid].volume = v

	@yt.command(pass_context=True)
	@player_exists()
	async def list(self, ctx):
		sid = ctx.message.server.id
		if len(musicQue[sid]) > 0:
			returnS = '```xl\n'
			for i in musicQue[sid]:
				returnS += (i+'\n')
			returnS += '```'
			await self.bot.say('Current list of music in queue\n'+returnS)

	@yt.command(pass_context=True)
	@player_exists()
	async def song(self, ctx):
		sid = ctx.message.server.id
		await self.bot.say('Current song playing: **'+ player[sid].title+'**')


def setup(bot):
	bot.add_cog(musicbot(bot))
