import discord
from discord.ext import commands
from discord import app_commands

import config
from config import minimumPayout, payoutCurrency, minimumDeposit, depositLink, depositCurrency, errorColor, successColor


class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance")
    async def balance(self, ctx: discord.Interaction):
        userDocument = self.bot.get_user_document(ctx.user.id)

        if userDocument is None:
            return await self.bot.register_error(ctx)

        balanceEmbed = discord.Embed(title=f"{ctx.user.name}'s Wallet",
                                     description=f"Balance: ${userDocument['balance']}", colour=config.successColor)

        await ctx.response.send_message(embed=balanceEmbed)

    @app_commands.command(name="deposit", description="Add money into your wallet.")
    @app_commands.describe(amount="Enter the amount to deposit.")
    async def deposit(self, ctx: discord.Interaction, amount: int):
        userDocument = self.bot.get_user_document(ctx.user.id)
        if userDocument is None:
            return await self.bot.register_error(ctx)

        if amount < 5:
            embedError = discord.Embed(title="Deposit Error", description=f"Minimum deposit must be 5 {depositCurrency}.", color=errorColor)
            return await ctx.response.send_message(embed=embedError, ephemeral=True)

        link = depositLink.format(amount, depositCurrency)

        embedMessage = discord.Embed(title="Generated Deposit Link", description=f"Link: {link}", color=successColor)
        embedMessage.set_footer(text="Make sure to deposit using the same Paypal linked to your Discord account.")
        await ctx.response.send_message(embed=embedMessage)



    @app_commands.command(name="withdraw", description="Withdraw money from your wallet.")
    @app_commands.describe(amount="Enter the amount to be withdrawn (Enter 'all' to withdraw  all)")
    async def withdraw(self, ctx: discord.Interaction, amount: str):
        amount = amount.lower()

        userDocument = self.bot.get_user_document(ctx.user.id)
        if userDocument is None:
            return await self.bot.register_error(ctx)

        userBalance = userDocument["balance"]

        try:
            if amount == "all":
                payoutAmount = userBalance
            elif float(amount) <= userBalance:
                payoutAmount = float(f"{float(amount):.2f}")
            else:
                embedError = discord.Embed(title="Withdrawal Error", description="Not enough funds.", color=config.errorColor)
                return await ctx.response.send_message(embed=embedError, ephemeral=True)

        except Exception:
            embedError = discord.Embed(title="Withdrawal Error", description="Invalid Amount.", color=config.errorColor)
            return await ctx.response.send_message(embed=embedError, ephemeral=True)

        if payoutAmount < minimumPayout:
            embedError = discord.Embed(title="Withdrawal Error",
                                       description=f"Minimum withdrawal must be 5 {payoutCurrency}.", color=config.errorColor)
            return await ctx.response.send_message(embed=embedError, ephemeral=True)

        self.bot.update_user_balance(ctx.user.id, -payoutAmount)

        embedMessage = discord.Embed(title="Withdrawal Successful!",
                                     description=f"{payoutAmount} {payoutCurrency} will be deposited into your linked Paypal account within 5-10 minutes. Please be Patient",
                                     color=config.successColor)

        await ctx.response.send_message(embed=embedMessage)

        await self.bot._payoutUser(ctx.user, userDocument["paypalEmail"], payoutAmount)


async def setup(client):
    await client.add_cog(Currency(client))
