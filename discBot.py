# bot.py
import os
import random
import datetime
import re
import time
from timeit import repeat

import discord
from discord import file
from discord.channel import TextChannel
from discord.enums import MessageType
from discord.message import Message
from discord.voice_client import VoiceClient, VoiceProtocol
from dotenv import load_dotenv

t_offset = datetime.timedelta(hours = 3)

load_dotenv()
TOKEN = os.getenv('DAD_TOKEN')

repeatAh = 0
repeat20 = 0

game = 'GET OFF MY LAWN'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(activity=discord.Activity(type=discord.ActivityType.watching, name=game), intents=intents)

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
            # async for message in channel.history():
            #     if message.author == client.user and message.attachments[0].filename == 'ah_yes.webm':
            #         return
            await channel.send(file = discord.File('/root/dad_bot/media/ah_yes.webm'))
    else:
        repeatAh = 0

    if str((message.created_at + t_offset).weekday()) == '3' and str((message.created_at + t_offset).day) == '20':
        if repeat20 == 0:
            repeat20 = 1
            channel = client.get_channel(289773173384151040)
            await channel.send(file = discord.File('/root/dad_bot/media/thurs20.jpg'))
    else:
        repeat20 = 0

    ## Failed experiment, discord has too many edge cases that trigger this loop to make it worthwhile tryig to fix
    #if message.content.upper() == message.content and message.content != "_ _" and message.type != discord.MessageType.pins_add:
    #    id = '<@' + str(message.author.id) + ">"
    #    response = "KEEP IT DOWN " + id + "!"
    #    await message.channel.send(response)


#@client.event
#async def on_typing(channel, user='134546892750061569', time=datetime.datetime.now()):
#    id = "<@134546892750061569>"
#    x = random.randint(0,5)
#    if x == 0:
#        message = "shush " + id
#        print('in loop')
#        await channel.send(message)


""" CHRISTMAS MARIAH CAREY VOICE CHANNEL JOIN - DISABLED FOR NOW """
# @client.event
# async def on_voice_state_update(member, before, after):
#     ## Plays Mariah Carey when a user joins a voice channel
#     if after.channel != None:
#         connected = after.channel
#         voice = await connected.connect()
#         mariah(voice)
#         time.sleep(2)
#         await voice.disconnect()
    

# def mariah(voiceChannel):
#     currentDate = datetime.datetime.now()
#     weekdayNum = currentDate.strftime("%w")
#     if lastPlayed == weekdayNum:
#         return
#     if currentDate.hour < 9 or currentDate.month != 12 or currentDate.day < 20: ## Only plays between Dec 20 and Dec 25th (as files are named 1-5 for the days leading up to Xmas)
#         return
    
#     try:
#         mariahFile = f"/root/dad_bot/media/mariah{weekdayNum}.mp3"
#         audio_source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mariahFile))

#         voiceChannel.play(audio_source, after=None)
#         lastPlayed = weekdayNum
#     except Exception as e:
#         print(f"Error playing Mariah Carey: {e}")

client.run(TOKEN)
