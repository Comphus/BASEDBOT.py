import discord
from discord.ext import commands
import asyncio
import functools
import datetime
import audioop
import youtube_dl
import logging

logger = logging.getLogger('musicstuff')
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

#code taken from rewrite basic_voice.py example and modified
ytdl_format_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
	'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)

		self.data = data

		self.title = str(data.get('title','title not found'))
		self.url = str(data.get('url','url not found'))
		self.views = data.get('view_count',"0")
		self.likes = data.get('like_count',0)
		self.dislikes = data.get('dislike_count',0)

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]

		filename = data['url'] if stream else ytdl.prepare_filename(data)
		# beforeopt = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class musicbot(commands.Cog):
	"""
	makes music
	"""

	def __init__(self, bot):
		self.bot = bot
		self.musicQue = {}

	async def complete_stop(self, ctx, sid):
		try:
			ctx.voice_client.stop()	
		except:
			pass
		try:
			await ctx.voice_client.disconnect()
		except Exception:
			pass
		try:
			await self.bot.get_guild(sid).voice_client.disconnect()
		except:
			pass
		del self.musicQue[sid]
	
	async def runmusic(self, ctx, sid):
		if len(self.musicQue[sid]) == 0:
			await self.complete_stop(ctx, sid)
			await ctx.send("No more songs in queue")
			return
		if ctx.voice_client.is_playing() != None:
			ctx.voice_client.stop()
		plyr = await YTDLSource.from_url(self.musicQue[sid][0], loop=self.bot.loop, stream=True)
		ctx.voice_client.play(plyr, after=lambda e: print('Player error: %s' % e) if e else None)
		try:
			await ctx.send('**Playing:** __**{}**__\n**Views:** {:,}\n:thumbsup: : {:,}   :thumbsdown: : {:,}'.format(plyr.title, plyr.views, plyr.likes, plyr.dislikes))
		except:
			await ctx.send('**Playing:** __**{}**__\n**Views:** Unable to extract view-count data\n:thumbsup: : {:,}   :thumbsdown: : {:,}'.format(plyr.title, plyr.likes, plyr.dislikes))
		del self.musicQue[sid][0]
		while True:
			try:
				if not ctx.voice_client.is_playing() and ctx.voice_client.is_paused() == False:
					await self.runmusic(ctx, sid)
					break
			except:
				pass
			await asyncio.sleep(1)

	def cog_unload(self):
		for voice in self.bot.voice_clients:
			try:
				del self.musicQue[voice.guild.id]
				self.bot.loop.create_task(voice.disconnect())
			except:
				pass


	@commands.group(invoke_without_command=True)#main command
	async def yt(self, ctx, *, song : str):
		print("started music")
		#await ctx.send("the `!yt` function is currently under repair/rewriting and will be restarted several times for a bit")
		if ctx.message.guild.id not in self.musicQue and ctx.voice_client.is_playing() == False:
			self.musicQue[ctx.message.guild.id] = []
			self.musicQue[ctx.message.guild.id].append(song)
			print('started in '+ str(ctx.message.guild.id))
			try:
				print('guild name is: '+ str(ctx.message.guild.name))
			except:
				pass
			await self.runmusic(ctx, ctx.message.guild.id)
			return

		await ctx.send('Enqueued **{}**'.format(song))
		self.musicQue[ctx.message.guild.id].append(song)


	@yt.command(pass_context=True, no_pm=True)
	async def summon(self, ctx):
		"""Summons the bot to join your voice channel."""
		summoned_channel = ctx.message.author.voice.channel
		if summoned_channel is None:
			await ctx.send('You are not in a voice channel.')
			return False

		if ctx.voice_client is not None:
			return await ctx.voice_client.move_to(summoned_channel)
		await summoned_channel.connect()

	@yt.command()#all sub commands from here and below
	async def help(self, ctx):
		await ctx.send('How to make the !yt function work, type in \'!yt \', then whatever url you want afterwards to make it play its audio, will not play from ALL links.\n__Commands you can put in after !yt for !yt are:__\n**next/skip** - goes to the next song, if there isnt one then the bot leaves\n**list** - a list of songs in queue\n**song** - current song playing\n**pause/resume** - pauses or resumes the song\n**stop** - stops the music bot and removes it from the channel, use this incase it breaks, or to end the session\n**volume** - can change volume of bot to either 0 or 200%, ex: !yt volume 50\n**help** - pulls up this text')

	@yt.command(pass_context=True)
	async def stop(self, ctx):
		await self.complete_stop(ctx, ctx.message.guild.id)
		print('Used !stop in: ' + str(ctx.message.guild.id))

	@yt.command(aliases=['next'], pass_context=True)
	async def skip(self, ctx):
		if ctx.voice_client.is_connected():
			ctx.voice_client.stop()

	@yt.command(pass_context=True)
	async def pause(self, ctx):
		if ctx.voice_client.is_connected():
			ctx.voice_client.pause()

	@yt.command(pass_context=True)
	async def resume(self, ctx):
		if ctx.voice_client.is_connected():
			ctx.voice_client.resume()

	@yt.command(pass_context=True, aliases=['vol'])
	async def volume(self, ctx, vol : int):
		sid = ctx.message.guild.id
		if vol > 200 or vol < 0:
			await ctx.send('volume number must be between 0 and 200')
		else:
			v = (vol/100.0)
			ctx.voice_client.source.volume = v

	@yt.command(pass_context=True)
	async def list(self, ctx):
		sid = ctx.message.guild.id
		if len(self.musicQue[sid]) > 0:
			returnS = '```xl\n'
			for i, name in enumerate(self.musicQue[sid]):
				returnS += ("{}. {}\n".format(i+1,name))
			returnS += '```'
			await ctx.send('Current list of music in queue\n'+returnS)
		await ctx.send('Currently no music in queue.')

	@yt.before_invoke
	async def ensure_voice(self, ctx):
		if ctx.voice_client is None:
			if ctx.author.voice:
				await ctx.author.voice.channel.connect()
			else:
				await ctx.send("You are not in a voice channel, please join a voice channel in order to play music.")
				raise commands.CommandError("Author not connected to a voice channel.")


def setup(bot):
	bot.add_cog(musicbot(bot))