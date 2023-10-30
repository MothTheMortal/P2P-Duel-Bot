import discord
import pymongo.collection
from discord.ext import commands
from pymongo import MongoClient
import config


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
            "totalBetMoneyWon": 0,
            "totalTournamentMoneyWon": 0,
            "totalBets": 0,
            "totalTournaments": 0,
            "betsWon": 0,
            "tournamentsWon": 0
        }

        collection = self.get_database_collection("users")
        collection.insert_one(doc)

    def get_user_document(self, userID):
        collection = self.get_database_collection("users")
        return collection.find_one({"_id": str(userID)})

    @staticmethod
    def register_error(ctx: discord.Interaction):
        embed = discord.Embed(title="Unregistered User",description="Please do /register before using any other commands.", colour=0xFF0000)
        await ctx.response.send_message(embed=embed)
