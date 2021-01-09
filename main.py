import os
import discord
import pip
import time
import discord.client
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from itertools import cycle
import random

# client = authenticate_client()
# Confirming the name of my chosen server, if we want it for something specific.
GUILD = os.getenv('nwHacks Bot Server')
client = commands.Bot(command_prefix="~")  # This bot uses ~ to do commands.
token = 'Nzk3NTg3ODY5MTE5Njc2NDI3.X_oplg.S_88iTk6qPw1MKfEpz7NNOl9T3Y'

# -------------------
# On Ready Commands
# -------------------


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game('with your heart.'))
    change_status.start()

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
