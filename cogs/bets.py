import discord
from discord import app_commands
from discord.ext import commands
import config


class Bets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="register")
    async def test(self, ctx: discord.Interaction, email: str):
        await self.bot.insert_user_document(ctx.user, email)
        await ctx.response.send_message("Registered successfully!")


async def setup(client):
    await client.add_cog(Bets(client))
