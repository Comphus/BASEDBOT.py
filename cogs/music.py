import discord
from discord.ext import commands
import asyncio

class musicbot:
	"""
	makes music
	"""

	def __init__(self, bot):
		self.bot = bot
		self.opts = {
			'default_search': 'auto',
			'quiet': True,
		}
		self.player = {}
		self.musicQue = {}
		self.voice = {}
		self.chan = {}
		self.nexts = {}

	async def runmusic(self, sid):
		if len(self.musicQue[sid]) == 0:
			await self.bot.send_message(self.chan[sid], "No more songs in queue")
			await self.complete_stop(sid)
			return
		try:
			if self.player[sid] != None:
				self.player[sid].stop()
			self.player[sid] = await self.voice[sid].create_ytdl_player(self.musicQue[sid][0], ytdl_options=self.opts)
			self.player[sid].start()
			await self.bot.send_message(self.chan[sid], '**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(self.player[sid].title, self.player[sid].views, self.player[sid].likes, self.player[sid].dislikes))
		except Exception as e:
			await self.bot.send_message(self.chan[sid], str(e))
		del self.musicQue[sid][0]
		while True:
			if self.player[sid].is_done():
				await self.runmusic(sid)
				break
			await asyncio.sleep(1)

	def __unload(self):
		for voice in self.bot.voice_clients:
			try:
				await voice.disconnect()
			except:
				pass

	def create_music_setting(self, message):
		self.player[message.server.id] = None
		self.musicQue[message.server.id] = []
		self.nexts[message.server.id] = False
		self.chan[message.server.id] = message.channel

	@commands.group(pass_context=True, invoke_without_command=True)#main command
	async def yt(self, ctx, *, song : str):
		if self.voice.get(ctx.message.server.id) is None:
			success = await ctx.invoke(self.summon)
			if not success:
				await self.bot.say("You are not in a voice channel, please join a voice channel in order to play music.")
				return

		if ctx.message.server.id not in self.player:
			self.create_music_setting(ctx.message)
			self.musicQue[ctx.message.server.id].append(song)
			print('started in '+ ctx.message.server.id)
			try:
				print('server name is: '+ ctx.message.server.name)
			except:
				pass
			await self.runmusic(ctx.message.server.id)
			return

		if self.player[ctx.message.server.id] is None:
			self.create_music_setting(ctx.message)
		await self.bot.say('Enqueued **{}**'.format(song))
		self.musicQue[ctx.message.server.id].append(song)

	async def complete_stop(self, sid):
		try:
			self.player[sid].stop()	
		except:
			pass
		try:
			await self.voice[sid].disconnect()
		except Exception:
			pass
		try:
			await self.bot.voice_client_in(self.bot.get_server(sid)).disconnect()
		except:
			pass
		self.player[sid] = None
		self.musicQue[sid] = None
		self.voice[sid] = None
		self.chan[sid] = None
		del self.player[sid]
		del self.musicQue[sid]
		del self.voice[sid]
		del self.chan[sid]

	@yt.command(pass_context=True, no_pm=True)
	async def summon(self, ctx):
		"""Summons the bot to join your voice channel."""
		sid = ctx.message.server.id
		summoned_channel = ctx.message.author.voice_channel
		if summoned_channel is None:
			await self.bot.say('You are not in a voice channel.')
			return False

		state = self.voice.get(sid)
		if state is None:
			self.voice[sid] = await self.bot.join_voice_channel(summoned_channel)
		else:
			await self.voice[sid].move_to(summoned_channel)

		return True

	@yt.command()#all sub commands from here and below
	async def help(self):
		await self.bot.say('How to make the !yt function work, type in \'!yt \', then whatever url you want afterwards to make it play its audio, will not play from ALL links.\n__Commands you can put in after !yt for !yt are:__\n**next/skip** - goes to the next song, if there isnt one then the bot leaves\n**list** - a list of songs in queue\n**song** - current song playing\n**pause/resume** - pauses or resumes the song\n**stop** - stops the music bot and removes it from the channel, use this incase it breaks, or to end the session\n**volume** - can change volume of bot to either 0 or 200%, ex: !yt volume 50\n**help** - pulls up this text')

	@yt.command(pass_context=True)
	async def stop(self, ctx):
		await self.complete_stop(ctx.message.server.id)
		print('Used !stop in: ' + ctx.message.server.id)

	@yt.command(aliases=['next'], pass_context=True)
	async def skip(self, ctx):
		sid = ctx.message.server.id
		if self.voice[sid].is_connected():
			self.player[sid].stop()

	@yt.command(pass_context=True)
	async def pause(self, ctx):
		sid = ctx.message.server.id
		if self.voice[sid].is_connected():
				self.player[sid].pause()

	@yt.command(pass_context=True)
	async def resume(self, ctx):
		sid = ctx.message.server.id
		if self.voice[sid].is_connected():
				self.player[sid].resume()

	@yt.command(pass_context=True, aliases=['vol'])
	async def volume(self, ctx, vol : int = None):
		sid = ctx.message.server.id
		if vol is None or vol > 200 or vol < 0:
			await self.bot.say('volume number must be between 0 and 200')
		else:
			v = (vol/100.0)
			self.player[sid].volume = v

	@yt.command(pass_context=True)
	async def list(self, ctx):
		sid = ctx.message.server.id
		if len(self.musicQue[sid]) > 0:
			returnS = '```xl\n'
			for i, name in enumerate(self.musicQue[sid]):
				returnS += ("{}. {}\n".format(i+1,name))
			returnS += '```'
			await self.bot.say('Current list of music in queue\n'+returnS)

	@yt.command(pass_context=True, aliases=["playing"])
	async def song(self, ctx):
		sid = ctx.message.server.id
		if self.player.get(sid) is None:
			await self.bot.say('Not playing anything.')
		else:
			await self.bot.say('Current song playing: **'+ self.player[sid].title+'**')


def setup(bot):
	bot.add_cog(musicbot(bot))
