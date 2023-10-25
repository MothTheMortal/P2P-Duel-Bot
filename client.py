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

    #  Add utility and autonomous functions
