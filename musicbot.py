import discord
import asyncio
import codecs
import shelve
if not discord.opus.is_loaded():
	discord.opus.load_opus('opus')
client = discord.Client()


voice = None
player = None
songtoken = False
musicQue = []

@client.event
async def on_message(message):
	global voice
	global player
	global musicQue
	global songtoken


	if message.content.startswith('!chid'):
		await client.send_message(message.channel, message.channel.id)
	if True:
		if message.content.startswith("!yt") and len(message.content.split()) == 2:
			ctrC = message.content.lower().split()[1]
			musicControls = ["next", "skip", "list", "song","pause", "resume", "help"]
			if voice == None:
				try:
					voice = await client.join_voice_channel(message.author.voice_channel)
				except:
					await client.send_message(message.channel, "You are not in a voice channel, please join a voice channel in order to play music.")
					return
				#voice = await client.join_voice_channel(discord.utils.get(client.get_all_channels(), id ='129079702403940352'))
			if 'stop' in message.content:
				if voice.is_connected():
					await voice.disconnect()
					musicQue = []
					player = None
					voice = None
					songtoken = False
					return
			if ('next' in message.content or 'skip' in message.content) and player != None:
				if voice.is_connected():
					player.stop()
					if len(musicQue) == 0:
						await voice.disconnect()
						musicQue = []
					return
			if 'pause' in message.content and player != None:
				if voice.is_connected():
					player.pause()
					return
			if 'resume' in message.content and player != None:
				if voice.is_connected():
					player.resume()
					return
			if 'list' in message.content and player != None and len(musicQue) >0:
				returnS = ''
				for i in musicQue:
					if i not in musicControls:
						returnS += (i+'\n')
				await client.send_message(message.channel, 'Current list of music in queue\n\n'+returnS)
				returnS = ''
			if 'song' in message.content and player != None and len(musicQue) >0:
				await client.send_message(message.channel, 'Current song playing: **'+ player.title+'**')
			if 'help' in message.content:
				await client.send_message(message.channel, 'How to make the !yt function work, type in \'!yt \', then whatever url you want afterwards to make it play its audio, will not play from ALL links.\n__Commands you can put in after !yt for !yt are:__\n**next/skip** - goes to the next song, if there isnt one then the bot leaves\n**list** - a list of songs in queue\n**song** - current song playing\n**pause/resume** - pauses or resumes the song\n**stop** - stops the music bot and removes it from the channel, use this incase it breaks, or to end the session\n**help** - pulls up this text')
				if player == None:
					await voice.disconnect()
			async def playmusicque(voice, queurl):
				global musicon
				global player
				#global voice
				global currentsong
				global songtoken
				global extraQue
				try:
					if player != None:
						player.stop()
						player = await voice.create_ytdl_player(queurl)
						player.start()
						musicQue.pop(0)
						currentsong = (player.title)
						await client.send_message(message.channel, '**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(player.title, player.views, player.likes, player.dislikes))
						return
					else:
						player = await voice.create_ytdl_player(queurl)
						player.start()
						musicQue.pop(0)
						currentsong = (player.title)
						await client.send_message(message.channel, '**Playing:** __**{}**__\n**Views:** {}\n:thumbsup: : {}   :thumbsdown: : {}'.format(player.title, player.views, player.likes, player.dislikes))
						return
				except Exception as e:
					musicQue.pop(0)
					await client.send_message(message.channel, e)
					return

			if ctrC not in musicControls:
				endurl = message.content.split()[1]
				musicQue.append(endurl)
				#the loop
				if songtoken == False:
					songtoken = True
					while len(musicQue) >= 0:
						if player == None:
							print('anothertest')
							if len(musicQue) == 1:
								await playmusicque(voice, musicQue[0])
						await asyncio.sleep(2)
						print(musicQue)
						print("hello1")
						try:
							if player.is_done():
								print("hello2")
								if len(musicQue) == 0:
									await client.send_message(message.channel, "No more songs in queue")
									player = None
									await voice.disconnect()
									voice = None
									songtoken = False
									#print(songtoken)
									#break
								elif len(musicQue) > 0:
									#songtoken = True
									print("hello4")
									await playmusicque(voice, musicQue[0])
									#break
							
						except:
							pass
						
						
						try:
							if len(musicQue) == 0 and player.is_done():
								break
						except:
							pass
						if len(musicQue) == 0 and player == None:
							break
		elif message.content.startswith("!yt") and len(message.content.split()) != 2:
			await client.send_message(message.channel, 'You must have a link to show after !yt. It can be almost anything, youtube, soundcloud, even pornhub!')



@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	yield from client.change_status(game=discord.Game(name='with your mom'))

def main_task():
	yield from client.login('Your username', 'Your password')
	yield from client.connect()


loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(main_task())
except Exception:
	loop.run_until_complete(client.close())
finally:
	loop.close()
