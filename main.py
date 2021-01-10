from discord import guild, user
from firestore_methods import firestore_add, firestore_init, firestore_score_dict, pull_current_leader, set_current_leader, firestore_average_bubble
from azure_methods import sentiment_analysis, authenticate_client, sentiment_confidence
from array_functions import sortDictionary, bubblyRadar
import os
import discord
import discord.utils
import pip
import time
import discord.client
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from itertools import cycle
import json
import random
# import levelsys
# cogs = [levelsys]


# Azure Init
azure_client = authenticate_client()

# Firestore Init
firebase_db = firestore_init()

load_dotenv()
# client = authenticate_client()
# Confirming the name of my chosen server, if we want it for something specific.
GUILD = os.getenv('nwHacks Bot Server')
# This bot uses ~ to do commands.
intents = discord.Intents(messages=True, guilds=True,
                          reactions=True, members=True)
client = commands.Bot(command_prefix="~", intents=intents)
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

# Auto-role for members joining from Devpost


@client.event
async def on_member_join(ctx):
    autorole = discord.utils.get(ctx.guild.roles, name='Guest User')
    await ctx.add_roles(autorole)

# ------------------
# LEVELING
# ------------------
level = ["Bubblish, Bubblier, Bubbly, The Bubbliest"]
levelnum = [1, 2, 3, 4]

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
                    value='Shows the ranking of the most bubbly people in the server!', inline=False)
    embed.add_field(name='~score @name',
                    value='Returns how bubbly a specific server member is', inline=False)
    embed.add_field(name='~bubble @name',
                    value='Returns how bubbly you are in the server', inline=False)
    embed.add_field(name='~currentLeader',
                    value='Returns the most bubbly member in the current server.', inline=False)
    embed.add_field(name='~analysis <text>',
                    value='Analyze the sentiment of a specific string.', inline=False)
    embed.add_field(
        name='~ping', value='Return current bot latency', inline=False)
    embed.add_field(
        name='~clear #', value='Clear messages from current channel, where # = number of messages you wish to delete', inline=False)
    await ctx.send(embed=embed)


@client.command()
async def leaderboard(ctx):  # prettier version of help? Maybe later.

    author = ctx.message.author
    sorted_dict = sortDictionary(firestore_score_dict(firebase_db))
    embed = discord.Embed(
        colour=discord.Colour.blurple()
    )
    embed.set_thumbnail(
        url="https: // cdn.discordapp.com/attachments/797589271292805170/797623697049124874/nwhacks.png")
    embed = discord.Embed(title="------\nLEADERBOARD\n------", color=0xff40ff)
    count = 1
    for key in sorted_dict.keys():
        embed.add_field(name=f'{count}: {await client.fetch_user(key)}',
                        value=f'Score: {sorted_dict[key]}', inline=False)
        count += 1
        if (count >= 10):
            break
    await ctx.send(embed=embed)


@client.command()  # Find the current latency of the bot
async def ping(ctx):
    # latency in milliseconds
    await ctx.send(f'Bot ping is {round(client.latency * 1000)} ms')


@client.command()  # text
async def currentLeader(ctx):
    await ctx.send(f"The current leader is <@{pull_current_leader(firebase_db)}>!")


@client.command()  # text
async def analysis(ctx, *, a: str):
    print(a)
    statement = [str(a)]
    confidence = sentiment_confidence(azure_client, statement)
    await ctx.send(f"Positive: {confidence[0]}, Neutral: {confidence[1]}, Negative: {confidence[2]} ")


@client.command()
async def score(ctx, user: discord.Member):
    id = user.id
    sorted_dict = sortDictionary(firestore_score_dict(firebase_db))
    score = sorted_dict[str(id)]
    await ctx.send(f'User score is: {score}', delete_after=10)  # deletes after

# not working and i don't know why :(


@client.command()
async def bubble(ctx, user: discord.Member):
    id = user.id
    sorted_dict = sortDictionary(firestore_average_bubble(firebase_db))
    score = sorted_dict[str(id)]
    # message for checking if dictionary is working
    # # await ctx.send(sorted_dictionary)
    await ctx.send(f'Your average bubbly score is: {score} (out of a scale of 3!)')
    await ctx.send(f'You are considered {bubblyRadar(score)}!')


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
    ctx = await client.get_context(message)
    if (message.author.bot) != True:
        if "~" not in str(message.content):
            statement = [str(message.content)]
            confidence = sentiment_confidence(azure_client, statement)
            firestore_add(message.author.id, firebase_db, confidence)
            sorted_dict = sortDictionary(firestore_score_dict(firebase_db))
            # await message.channel.send(sorted_dict) - #message for checking if dictionary is working

            # check current leader
            first_key = int(next(iter(sorted_dict)))
            if (first_key != pull_current_leader(firebase_db)):
                role = discord.utils.get(message.guild.roles, name="Bubbliest")
                for m in ctx.guild.members:
                    await m.remove_roles(role)
                user = client.get_user(first_key)
                # await person.add_roles("Bubbliest")
                # member = guild.Member(next(iter(sorted_dict)))
                await message.author.add_roles(role)
                await message.channel.send(f"The new leader is <@{first_key}>!")
            set_current_leader(firebase_db, first_key, sorted_dict[next(
                iter(sorted_dict))])  # has to be updated every time

    if message.content == 'Hi':
        response = 'Hey'
        await message.channel.send(response)


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
# RUN BOT
# -------------
client.run(token)
