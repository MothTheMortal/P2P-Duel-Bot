import discord
from discord.ext import commands
import config


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(client):
    await client.add_cog(Currency(client))
