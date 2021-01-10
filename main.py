from azure_methods import sentiment_analysis, authenticate_client, sentiment_confidence
import os
import discord
import pip
import time
import discord.client
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from itertools import cycle
import json
import random
import levelsys
cogs = [levelsys]
# from firestore import firestore_init

# Azure Init
azure_client = authenticate_client()

# Firestore Init
# firestore_init()

load_dotenv()
# client = authenticate_client()
# Confirming the name of my chosen server, if we want it for something specific.
GUILD = os.getenv('nwHacks Bot Server')
# This bot uses ~ to do commands.
client = commands.Bot(command_prefix="~", intents=discord.Intents.all())
token = ''

# -------------------
# On Ready Commands
# -------------------

print('test')


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

# -------
# TASKS
# -------
botStatus1 = cycle(
    ['with your heart.', 'with your mind', 'with your feelings'])


@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(botStatus1)))

# ------------------
# COGS
# ------------------
for i in range(len(cogs)):
    print("temp")


# ------------------
# RANDOM COMMANDS
# ------------------
client.remove_command('help')


@client.command()
async def help(ctx):  # prettier version of help? Maybe later.
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed = discord.Embed(title="------\nHELP\n------", color=0xff40ff)
    embed.add_field(name='~leaderboard',
                    value='Create custom channel for sentiment scoring', inline=False)
    embed.add_field(name='~score @name',
                    value='Returns the score of a specific server member', inline=False)
    embed.add_field(name='~score @role',
                    value='Returns the score of a specific server role', inline=False)
    embed.add_field(
        name='~ping', value='Return current bot latency', inline=False)
    embed.add_field(
        name='~clear #', value='Clear messages from current channel, where # = number of messages you wish to delete', inline=False)
    await ctx.send(embed=embed)


@client.command()  # Find the current latency of the bot
async def ping(ctx):
    # latency in milliseconds
    await ctx.send(f'Bot ping is {round(client.latency * 1000)} ms')


@client.command()  # text
async def niceMsg(ctx):
    await ctx.send(f'Annie & Ella are amazing and Johnny is not.')


@client.command()  # clear a channels messages.
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):  # default 1 message if not specified
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'**[ {amount} ] messages have been yeeted.**')
    time.sleep(2)  # 5 second delay for message above.
    await ctx.channel.purge(limit=1)

# -------------
# ON MESSAGE
# -------------


@client.event
async def on_message(message):
    await client.process_commands(message)

    if (message.author.bot) != True:
        if ctx.channel.name == ("bot-test"):
            statement = [str(message.content)]
            # response = sentiment_analysis(azure_client, statement)
            # confidence = sentiment_confidence(azure_client, statement)
            # await message.channel.send(response)
            # await message.channel.send(confidence)
            await message.channel.send(message.author.id)

    if message.content == "type?":
        response = str(message)
        response = type(response)
        await message.channel.send(response)

    if message.content.lower() == 'what team?':
        response = 'Wildcats!'
        await message.channel.send(response)

    if message.content == 'Hi':
        response = 'Hey'
        await message.channel.send(response)

    # if message.content == 'Annie hates Johnny.':
    #     await message.channel.send(response)


def new_func(message):
    message = message.lower()
    return message

# -----------------
# ERROR HANDLING
# -----------------


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('You did not use a valid command, silly billy.')

# -------------
# VOICE
# -------------


@client.command()
async def join_voice(self, ctx):
    channel = ctx.author.voice.channel
    print(channel.id)
    await self.client.VoiceChannel.connect()


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


# -------------
# RUN BOT
# -------------
client.run(token)
