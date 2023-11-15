import discord
import pymongo.cursor
from discord.ext import commands, tasks
from discord import app_commands
import config
from pymongo.collection import Collection


class CogManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.depositHandler.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}")
        synced = await self.bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
        await self.depositHandler()

    @tasks.loop(seconds=5)
    async def depositHandler(self):
        collection: Collection = self.bot.get_database_collection("deposits")

        docs = collection.find({"userID": ""})

        for doc in docs:
            print("Processing...")
            userDoc = self.bot.get_user_document_with_email(doc["senderEmail"])

            if userDoc is None:
                return

            userID = userDoc["_id"]
            user = await self.bot.fetch_user(userID)

            if doc["currency"] != "USD":
                errorEmbed = discord.Embed(title="Deposit Error", description=f"Invalid Currency Deposited\nExpected: USD\nReceived: {doc['currency']}", colour=config.errorColor)
                errorEmbed.set_footer(text="Please contact a staff for a refund.")
                collection.update_one({"_id": doc["_id"]}, {"$set": {"userID": userID}})
                return await self.bot.dm_user(user, embed=errorEmbed)

            self.bot.update_user_balance(userID, doc['actualAmount'])
            embedMessage = discord.Embed(title="Deposit Complete", description=f"{doc['actualAmount']} {doc['currency']} has been deposited into your wallet.", color=config.successColor)
            embedMessage.set_footer(text=f"Deposit has been subjected to {round(doc['feePercentage'], 1)}% transaction fee.")

            collection.update_one({"_id": doc["_id"]}, {"$set": {"userID": userID}})
            await self.bot.dm_user(user, embed=embedMessage)

    @tasks.loop(seconds=5)
    async def payoutHandler(self):
        collection: Collection = self.bot.get_database_collection("payouts")

        docs = collection.find({"userID": ""})

        for doc in docs:
            print("Processing...")
            userDoc = self.bot.get_user_document_with_email(doc["receiverEmail"])

            if userDoc is None:
                return

            userID = userDoc["_id"]
            collection.update_one({"_id": doc["_id"]}, {"$set": {"userID": userID}})

            embedMessage = discord.Embed(title="Withdrawal Complete",
                                         description=f"{doc['actualAmount']} {doc['currency']} has been deposited into your wallet.",
                                         color=config.successColor)
            user = await self.bot.fetch_user(userID)

            await self.bot.dm_user(user, embed=embedMessage)



    @app_commands.command(name="register")
    @app_commands.describe(paypal_email="Enter your Paypal Email.")
    async def register(self, ctx: discord.Interaction, paypal_email: str):
        if self.bot.get_user_document(ctx.user.id) is not None:
            embedError = discord.Embed(title="Registration Error", description="User is already registered.",
                                       color=config.errorColor)
            return await ctx.response.send_message(embed=embedError, ephemeral=True)

        if self.bot.get_user_document_with_email(paypal_email) is not None:
            embedError = discord.Embed(title="Registration Error", description="Paypal Email is already in use.",
                                       color=config.errorColor)
            return await ctx.response.send_message(embed=embedError, ephemeral=True)

        if not config.checkEmail(paypal_email):
            embedError = discord.Embed(title="Registration Error", description="Invalid Email Format.",
                                       color=config.errorColor)
            return await ctx.response.send_message(embed=embedError, ephemeral=True)

        self.bot.insert_user_document(ctx.user, paypal_email)

        embedMessage = discord.Embed(title="Registration Successful", description="User has successfully registered!",
                                     color=config.successColor)
        await ctx.response.send_message(embed=embedMessage, ephemeral=True)


async def setup(client):
    await client.add_cog(CogManager(client))
