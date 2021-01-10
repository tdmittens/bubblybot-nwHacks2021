import discord
from discord.ext import commands
from firebase_admin.firestore import client

bot_channel = 797591093632958486
talk_channel = 797716161617068032

level = ["Bubblish, Bubblier, Bubbly, The Bubbliest"]
levelnum = [1, 2, 3, 4]

cluster = MongoClient("MONGO_DB_ADDRESS_HERE")

levelling = cluster["discord"]["levelling"]


class levelsys(commands.Cog):
    def_init_(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on
