import discord
from discord.ext import commands
from discord import app_commands
import config


class CogManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}")
        synced = await self.bot.tree.sync()
        print(f"Synced {len(synced)} commands.")

    @app_commands.command(name="register")
    @app_commands.describe(paypal_email="Enter your Paypal Email.")
    async def register(self, ctx: discord.Interaction, paypal_email: str):

        if self.bot.get_user_document(ctx.user.id) is not None:
            embedError = discord.Embed(title="Registration Error", description="User is already registered.", color=0xFF0000)
            return await ctx.response.send_message(embed=embedError, ephemeral=True)

        self.bot.insert_user_document(ctx.user, paypal_email)

        embedMessage = discord.Embed(title="Registration Successful", description="User has successfully registered!", color=0xFF0000)
        await ctx.response.send_message(embed=embedMessage, ephemeral=True)






async def setup(client):
    await client.add_cog(CogManager(client))
