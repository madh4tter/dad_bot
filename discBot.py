# bot.py
import os
import random
import datetime
import re
import time
from timeit import repeat

import gtts
from playsound import playsound

import discord
from discord import file
from discord.channel import TextChannel
from discord.enums import MessageType
from discord.message import Message
from dotenv import load_dotenv

t_offset = datetime.timedelta(hours = 3)

load_dotenv()
TOKEN = os.getenv('DAD_TOKEN')

repeatAh = 0
repeat20 = 0

game = 'GET OFF MY LAWN'
client = discord.Client(activity=discord.Activity(type=discord.ActivityType.watching, name=game))

@client.event
async def on_message(message):
    global repeatAh
    global repeat20
    if message.author == client.user:
        return

    if message.content.startswith("!joke"):
        with open('jokes.txt', encoding="UTF-8") as f:
            lines = f.readlines()
            pre = random.choice(lines)
            pre = pre.split("||")
            output = pre[0].strip() + "\n" + pre[1].strip()
            await message.channel.send(output)

    check = re.compile(r"\A[Ii][']?[mM]\s")
    match = check.search(message.content[:4])
    if match:
        response = "Hi " + str(message.content[3:]).strip() + ", I'm Dad!"
        await message.channel.send(response)
  
    if str((message.created_at + t_offset).weekday()) == '5':
        if repeatAh == 0:
            repeatAh = 1
            channel = client.get_channel(289773173384151040)
            await channel.send(file = discord.File('/root/dad_bot/ah_yes.webm'))
    else:
        repeatAh = 0

    if str((message.created_at + t_offset).weekday()) == '3' and str((message.created_at + t_offset).day) == '20':
        if repeat20 == 0:
            repeat20 = 1
            channel = client.get_channel(289773173384151040)
            await channel.send(file = discord.File('/root/dad_bot/thurs20.jpg'))
    else:
        repeat20 = 0

    ## Failed experiment, discord has too many edge cases that trigger this loop to make it worthwhile tryig to fix
    #if message.content.upper() == message.content and message.content != "_ _" and message.type != discord.MessageType.pins_add:
    #    id = '<@' + str(message.author.id) + ">"
    #    response = "KEEP IT DOWN " + id + "!"
    #    await message.channel.send(response)

@client.event
async def on_voice_state_update(member, before, after):
    x = random.randint(0, 49)
    if after.channel != None and x == 0:
        connected = after.channel
        time.sleep(1)
        vc = await discord.VoiceChannel.connect(connected)
        voiceString = str(member.display_name) + ", please be quiet"
        print(voiceString)
        tts = gtts.gTTS(voiceString)
        tts.save("test.mp3")
        audio_source = discord.FFmpegPCMAudio("test.mp3")
        vc.play(audio_source, after=None)
        time.sleep(3)
        guild = member.guild.voice_client
        os.remove("test.mp3")
        await discord.VoiceClient.disconnect(guild)        

#
#@client.event
#async def on_typing(channel, user='134546892750061569', time=datetime.datetime.now()):
#    id = "<@134546892750061569>"
#    x = random.randint(0,5)
#    if x == 0:
#        message = "shush " + id
#        print('in loop')
#        await channel.send(message)

client.run(TOKEN)
