# bot.py
from asyncio import tasks
from asyncio.tasks import gather
import os
import random
import re

import discord
from discord import channel
from discord import message
from discord import activity
import requests
from discord.ext import commands
from discord import file
from discord.channel import TextChannel
from discord.enums import MessageType
from discord.message import Message
import shutil
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('CARE_TOKEN')

game = 'cleaning up peoples shit'
bot = commands.Bot(command_prefix='', activity=discord.Game(name=game))


@bot.event
async def on_message(message):
    global repeat
    if message.author == bot.user:
        return

    check = re.compile(r"(http[s]*://p.*[.]jpg)")
    match = check.search(message.content)
    if match:
        msg = message.content
        if "||" in message.content: spoiler = True 
        else: spoiler = False
        out = msg.replace(match[0], '')
        out = out.strip()
        id = '<@' + str(message.author.id) + ">"
        img = match[0]
        file = img.split("/")[-1]

        if spoiler:
            file = f"SPOILER_{file}"

        r = requests.get(img, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True

            with open(file, 'wb') as f:
                shutil.copyfileobj(r.raw, f) 
        else:
            await channel.send("pic not found")
            return

        with open(file, 'rb') as g:
            outStr = '"' + out + '"' + ' - ' + id
            if out == "" or out == "||||":
                outStr = id
            await tasks.gather(message.channel.send(file=discord.File(g)), message.delete(), message.channel.send(outStr))
    
    
    path = os.listdir()
    for item in path:
        if item.endswith(".jpg"):
            os.remove(item)


bot.run(TOKEN)