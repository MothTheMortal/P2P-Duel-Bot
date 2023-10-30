import discord
from discord.ext import commands
from discord import app_commands
import config


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="balance")
    async def balance(self, ctx: discord.Interaction):
        userDocument = self.bot.get_user_document(ctx.user.id)

        if userDocument is None:
            return self.bot.register_error(ctx)

        balanceEmbed = discord.Embed(title=f"{ctx.user.name}'s Wallet", description=f"Balance: {userDocument['balance']}", colour=0xFF0000)

        await ctx.response.send_message(embed=balanceEmbed)


    @app_commands.command(name="withdraw")
    async def withdraw(self):
        ...


async def setup(client):
    await client.add_cog(Currency(client))
