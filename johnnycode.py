@client.command()
async def score(ctx, member: discord.Member):
    await ctx.send(f'{member.mention} has a total sentiment score of.')


@client.command()
async def score(ctx, role: discord.Role:
    await ctx.send(f'{role.mention} has an average sentiment score of.')

@ client.command()
async def help(ctx):  # prettier version of help? Maybe later.
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed = discord.Embed(title="------\nHELP\n------", color=0xff40ff)
    embed.add_field(
        name='~ping', value='Return current bot latency', inline=False)
    embed.add_field(
        name='~ping', value='Return current bot latency', inline=False)
    await ctx.send(embed=embed)
