from discord import Intents
from dotenv import load_dotenv
from os import getenv
from client import DuelBot


if __name__ == "__main__":
    load_dotenv()
    bot = DuelBot(command_prefix=".", intents=Intents.all(), help_command=None, mongodb_key=getenv("MONGODB"))
    bot.run(getenv("BOT_TOKEN"))