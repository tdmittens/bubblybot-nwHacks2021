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

from azure import sentiment_analysis, authenticate_client

# Azure Init
azure_client = authenticate_client()

load_dotenv()
# client = authenticate_client()
# Confirming the name of my chosen server, if we want it for something specific.
GUILD = os.getenv('nwHacks Bot Server')
client = commands.Bot(command_prefix="~")  # This bot uses ~ to do commands.
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
        f'{client.user} is connec ted to the following guild:\n'
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
    if message.author == client.user:
        return

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

    if message.content == 'Annie hates Johnny.':
        statement = [str(message.content)]
        response = sentiment_analysis(azure_client, statement)
        await message.channel.send(response)


def new_func(message):
    message = message.lower()
    return message

# -----------------
# ERROR HANDLING
# -----------------


@ client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('You did not use a valid command, silly billy.')

# -------------
# VOICE
# -------------


@ client.command()
async def joinvoice(ctx):
    connected = ctx.author.voice
    if connected:
        await connected.channel.connect()


@ client.command(pass_context=True)
async def leavevoice(ctx):
    connected = ctx.author.voice
    if connected:
        await connected.channel.disconnect()


# -------------
# RUN BOT
# -------------
client.run(token)
