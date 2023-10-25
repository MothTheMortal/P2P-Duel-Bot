import discord
from discord.ext import commands
import config


class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(client):
    await client.add_cog(Tournament(client))
