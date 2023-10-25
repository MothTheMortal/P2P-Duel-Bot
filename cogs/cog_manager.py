import discord
from discord.ext import commands
import config


class CogManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}")

        synced = await self.bot.tree.sync()
        print(f"Synced {len(synced)} commands.")



async def setup(client):
    await client.add_cog(CogManager(client))
