# bot.py
import os
import random
import datetime
import re

import discord
from discord import file
from discord.channel import TextChannel
from dotenv import load_dotenv

t_offset = datetime.timedelta(hours = 17)
repeat = 0

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_message(message):
    global repeat
    if message.author == client.user:
        return

    check = re.compile(r"\A[Ii][']?[mM]\s")
    match = check.search(message.content[:4])
    if match:
        response = "Hi " + str(message.content[3:]).strip() + ", I'm Dad!"
        await message.channel.send(response)
  
    if str((message.created_at + t_offset).weekday()) == '5':
        if repeat == 0:
            repeat = 1
            channel = client.get_channel(289773173384151040)
            await channel.send(file = discord.File('ah_yes.webm'))
    else:
        repeat = 0
        
    if message.content().upper() == message.content():
        response = "KEEP IT DOWN " + message.author() + "!"
        await channel.send(response)

@bot.command(name='joke', help='Responds with a randomly selected dad joke')
async def joke(ctx):
        with open('jokes.txt', encoding="UTF-8") as f:
            lines = f.readlines()
            pre = random.choice(lines)
            pre = pre.split("||")
            output = pre[0].strip() + "\n" + pre[1].strip()
            await ctx.channel.send(output)

    

bot.run(TOKEN)
