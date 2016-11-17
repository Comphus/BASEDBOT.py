import discord
import asyncio
import json
import datetime
import random

from BASEDBOTgames import *
from BASEDBOTbns import *
from BASEDBOTow import *
from BASEDBOTdn import *
from BASEDBOTetc import *
from BASEDBOTmusic import *
import BASEDBOTdiscord
client = discord.Client()

with open("C:/discordlogin.json") as j:
	dLogin = json.load(j)

@client.event
async def on_member_join(member):
	await BASEDBOTdiscord.newmem(client, member).newmember()

@client.event
async def on_member_update(before, after):
	if before.server.id == '106293726271246336':
		if len(before.roles) == len(after.roles):
			for i in after.roles:
				if i.name == 'Streamer':
					try:
						if after.game.type == 1:
							strm = streamer(client, after).DNstream()
							await strm
					except:
						pass

@client.event
async def on_message(message):
	if client.user == message.author or message.channel.id == '168949939118800896' or message.author.id in '128044950024617984':
		return

	#basedbot discord commands
	bbd = BASEDBOTdiscord.bbDiscord(client, message)
	if message.content.startswith('!debug') and message.author.id == '90886475373109248':
		await bbd.debug()
	elif message.content.startswith('!removeallmsgs') and message.author.id == '90886475373109248':
		await bbd.removeallmsgs()
	elif message.content.startswith('!vanish') and message.content.split()[2].isdigit() and len(message.mentions) > 0:
		await bbd.vanish()
	elif message.content.startswith('!totalmem'):
		await client.send_message(message.channel, "**Total Members:** {}".format(message.channel.server.member_count))
	elif message.content.startswith("!voiceid"):
		await client.send_message(message.channel, message.author.voice_channel.id)
	elif message.content.startswith("!stats"):
		await bbd.dStats()
	elif message.content.startswith('!id'):
		await bbd.dID()
	elif message.content.startswith('!myinfo'):
		await bbd.myinfo()
	elif message.content.startswith('!info') and len(message.content.split()) > 1:
		await bbd.info()
	elif message.content.startswith('!avatar'):
		await bbd.avatar()
	elif message.content.startswith('!serverpic'):
		await client.send_message(message.channel, message.channel.server.icon_url)
	elif message.content.startswith('!chid'):
		await client.send_message(message.channel, message.channel.id)
	elif message.content.startswith('!serverid'):
		await client.send_message(message.channel, message.channel.server.id)
	if message.channel.is_private == False and message.server.id == '106293726271246336': #main server commands
		await bbd.logmessage()
		if bbd.slowM() == True:
			await bbd.startslowmode()
		elif message.content.startswith('!slowmode'):
			await bbd.slowmode()
		""" DISABLED UNTIL MONTHLY KARAOKE STARTS
		elif message.content.startswith("!raisehand"):
			await bbd.raisehand()
		elif message.content.startswith('!klist'):
			await bbd.klist()
		elif message.content.startswith('!kskip'):
			await bbd.kskip()
		"""

	#music bot
	if message.content.startswith("!yt"):
		await musicbot(client).playmusic(message, message.server.id)

	#dn commands
	dn = dragonnest(client, message)
	if message.content.lower().startswith('!pug') and message.channel.id != '106293726271246336' and message.channel.server.id == '106293726271246336':
		await dn.onoffrole('pug')
	elif message.content.lower().startswith('!trade') and message.channel.id != '106293726271246336':
		await dn.onoffrole('trade')
	elif message.content.lower().startswith('!pvp') and message.channel.id != '106293726271246336':
		await dn.onoffrole('pvp')
	elif message.content.startswith('!viewer') and message.server.id == '106293726271246336':
		await dn.onoffrole('viewer')
	elif '@pug' in message.clean_content and message.channel.id != '106300530548039680' and message.channel.server.id == '106293726271246336':
		await dn.roleMention('pug')
	elif '@trade' in message.clean_content and message.channel.id != '106301265817931776' and message.channel.server.id == '106293726271246336':
		await dn.roleMention('trade')
	elif '@pvp' in message.clean_content and message.channel.id != '106300621459628032' and message.channel.server.id == '106293726271246336':
		await dn.roleMention('pvp')
	elif '@viewer' in message.clean_content and message.channel.server.id == '106293726271246336':
		await dn.roleMention('viewer')
	elif message.content.lower().startswith('!skillbuilds') or message.content.lower().startswith('!krskillbuilds'):
		await client.send_message(message.channel, dn.skillbuilds())
	elif message.content.startswith('!savednbuild'):
		await client.send_message(message.channel, dn.savednbuild())
	elif message.content.startswith('!editdnbuild'):
		await client.send_message(message.channel, dn.editdnbuild())
	elif message.content.startswith('!deletednbuild'):
		await client.send_message(message.channel, dn.deletednbuild())
	elif message.content.startswith('!mydnbuilds'):
		await dn.mydnbuilds()
	elif message.content.startswith('$') and len(message.content.split()) == 1:
		await dn.customdncommands()
	elif message.content.lower().startswith('!enhance') and message.channel.id != '106293726271246336':
		await dn.enhancement()
	elif message.content.lower().replace(' ', '') == '!sa':
		await dn.SA()
	elif message.channel.id == '107718615452618752': # skill-builds channel auto skill build distributor
		await dn.autobuilds()

	#overwatch commands
	ow = overwatch(client, message)
	if len(message.content.split()) > 1 and message.content.lower().split()[0] == '!ow' and message.channel.id != '106293726271246336':
		await client.send_message(message.channel, ow.owcheck(message.content[4:]))
		return
	elif message.content.startswith('|trivia') and ow.tCheck(message.server.id) != True and message.channel.id != '106293726271246336':
		await ow.trivia(message.server.id)
	elif message.content.startswith('|stop') and message.channel.id != '106293726271246336':
		await ow.stopTrivia(message.server.id)
	elif message.content.startswith('|points') and message.channel.id != '106293726271246336':
		await ow.points(message.server.id)

	#BNS commands
	bns = bladeandsoul(client, message)
	if message.content.startswith('!bnstree'):
		await client.send_message(message.channel, bns.bnstree())
	elif message.content.startswith('!bnsmarket'):
		await bns.bnsmarket()
	elif message.content.lower().startswith('!bns') and message.channel.id != '106293726271246336 88422130479276032 124934505810100224 146298657765851137 144803652635328512':
		await client.send_message(message.channel, bns.bnssearch())
	elif message.content.startswith('!savebnsbuild'):
		await client.send_message(message.channel, bns.savebnsbuild())
	elif message.content.startswith('!editbnsbuild'):
		await client.send_message(message.channel, bns.editbnsbuild())
	elif message.content.startswith('!deletebnsbuild'):
		await client.send_message(message.channel, bns.deletebnsbuild())
	elif message.content.startswith('!mybnsbuilds'):
		await bns.mybnsbuilds()
	elif message.content.startswith('!!'):
		await bns.prefixbnscommands()

	if message.content.startswith('!donkayme'):#these are random ass test commands
		await client.add_reaction(message, "🇩")
		await client.add_reaction(message, "🇴")
		await client.add_reaction(message, "🇳")
		await client.add_reaction(message, "🇰")
		await client.add_reaction(message, "🇦")
		await client.add_reaction(message, "🇾")
	if message.content.startswith('!boop'):
		await client.add_reaction(message, "🅱")
		await client.add_reaction(message, "🅾")
		await client.add_reaction(message, "🇴")
		await client.add_reaction(message, "🅿")
	if message.content.startswith('!bruh') and message.channel.id != '106293726271246336':
		s = '🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 🇮 🇯 🇰 🇱 🇲 🇳 🇴 🇵 🇶 🇷 🇸 🇹 🇺 🇻 🇼 🇽 🇾 🇿 😂 👌'
		n = s.split()
		for i in range(15):
			r = random.randint(0, len(n)-1)
			await client.add_reaction(message, n[r])

	#games
	g = games(client, message)
	if message.content in unicodeResponses:
		await client.send_message(message.channel, unicodeResponses[message.content.lower().split()[0]])
	elif message.content.startswith('!c4'):
		await g.c4()
	elif message.content.startswith('!duel') and str(message.channel.id) not in '91518345953689600 106293726271246336':    
		await g.duel()
	elif message.content.lower().startswith('!rps'):
		await g.rps()
	elif message.content.startswith('!shoot') and len(message.content.split()) == 2:
		await g.shoots()
	elif message.content.startswith('!trivia') and message.channel.id != '106293726271246336':
		await g.dntrivia()

	#other commands
	etc = botetc(client, message)
	if message.content.startswith('!'):
		await etc.mainprefixcommands()
	if '!' in message.content and message.channel.is_private == False and message.server.id not in '119222314964353025':
		await etc.zealemotes()
	if message.content.startswith('<@175433427175211008>'):
		await etc.bbresponse()
	elif message.content.startswith('!define') and message.channel.id != '106293726271246336':
		await client.send_message(message.channel, etc.defines())
	elif message.content.lower().startswith('!mal') and message.channel.id not in '106293726271246336':
		await client.send_message(message.channel, etc.mal())
	elif message.content.startswith('!checktwitch'):
		await client.send_message(message.channel, etc.checktwitch())
	elif message.content.startswith('!spookme'):
		await etc.spookme()
	elif message.content.startswith('!delete ian'):
		await etc.deleteian()
	elif message.content.startswith('!lightproc'):
		await etc.lightproc()
	elif message.content.startswith('!yesh') and message.server.id == '90944254297268224':
		await client.send_message(message.channel, """<:Heck1:235258589621649408><:Heck2:235258604448382978><:Fucking:235256098427240451>\n<:Heck4:235258621955407872><:Man:235256139514773504><:Im:235256149455273984>\n<:Fuckin:235256165804539906><:Cumming:235256179045957633><:Cx:235256191154913280>""")
	elif message.content.startswith('!gimmepoutine'):
		await client.send_file(message.channel, 'poutine.jpg')
	elif (message.content.lower().startswith('!colors') or message.content.lower().startswith('!colorlist')) and message.channel.is_private == False and message.server.id == '106293726271246336':
		await etc.colors()
	elif message.content.lower().startswith('!color') and message.channel.is_private == False and message.server.id == '106293726271246336':
		await etc.color()
	

@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	yield from client.change_presence(game=discord.Game(name='you like a fiddle'))
	BASEDBOTdiscord.upT = datetime.now()

async def main_task():
	await client.login(dLogin['username'])
	await client.connect()

loop = asyncio.get_event_loop()
try:
	loop.run_until_complete(main_task())
except Exception:
	loop.run_until_complete(client.close())
finally:
	loop.close()
