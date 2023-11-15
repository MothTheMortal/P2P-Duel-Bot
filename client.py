import discord
import pymongo.collection
from discord.ext import commands
from pymongo import MongoClient
import config
import time
from payouts import userPayout


class DuelBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.database = MongoClient(kwargs["mongodb_key"])[config.database_name]

    async def setup_hook(self) -> None:
        for cog in config.cogs:
            await self.load_extension(f"cogs.{cog}")

    def get_database_collection(self, collection):
        return self.database[collection]

    #  Add utility and autonomous functions

    def insert_user_document(self, user, email):
        doc = {
            "_id": str(user.id),
            "balance": 0,
            "paypalEmail": email,
            "unixTime": str(time.time()),
            "totalBetMoneyWon": 0,
            "totalTournamentMoneyWon": 0,
            "totalBets": 0,
            "totalTournaments": 0,
            "betsWon": 0,
            "tournamentsWon": 0,
            "totalDeposited": 0,
            "totalWithdrawn": 0
        }

        collection = self.get_database_collection("users")
        collection.insert_one(doc)

    def insert_payout_document(self, data, receiver, amount, userID):
        collection = self.get_database_collection("payouts")
        doc = {
            "userID": str(userID),
            "batchID": data["batch_header"]["payout_batch_id"],
            "itemIDs": data["batch_header"]["sender_batch_header"]["sender_batch_id"],
            "receiverEmail": receiver,
            "amount": amount,
            "unixTime": str(time.time())
        }
        collection.insert_one(doc)

    def get_user_document(self, userID):
        collection = self.get_database_collection("users")
        return collection.find_one({"_id": str(userID)})

    def get_user_document_with_email(self, email):
        collection = self.get_database_collection("users")
        return collection.find_one({"paypalEmail": email})

    def update_user_balance(self, userID, amount):
        collection = self.get_database_collection("users")
        collection.update_one({"_id": str(userID)}, {"$inc": {"balance": round(amount, 2)}})

    async def _payoutUser(self, user, receiver, amount):
        data = userPayout(receiver, amount)
        if data:
            # self.insert_payout_document(data, receiver, amount, user.id)
            embed = discord.Embed(title="Withdrawal Complete", description=f"{amount} {config.payoutCurrency} have been sent to your linked Paypal account!", color=config.successColor)
            await self.dm_user(user, embed=embed)

    @staticmethod
    async def dm_user(user: discord.User, text="", embed=None):
        dm_channel = user.dm_channel
        if dm_channel is None:
            dm_channel = await user.create_dm()
        await dm_channel.send(content=text, embed=embed)

    @staticmethod
    async def register_error(ctx: discord.Interaction):
        embed = discord.Embed(title="Unregistered User", description="Please do /register before using any other commands.", colour=config.errorColor)
        await ctx.response.send_message(embed=embed, ephemeral=True)
