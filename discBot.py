# bot.py
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith("I'm ") or message.content.startswith("im ") or message.content.startswith("i'm ") :
        response = "Hi " + str(message.content[3:]).strip() + ", I'm dad!"
        await message.channel.send(response)

client.run(TOKEN)