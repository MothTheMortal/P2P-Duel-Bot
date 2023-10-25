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
