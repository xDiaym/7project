import os

from dotenv import load_dotenv

load_dotenv()


class BotConfig:
    ID = int(os.environ.get("BOT_ID"))
    TOKEN = os.environ.get("BOT_TOKEN")


class DatabaseConfig:
    NAME = os.environ.get("DB_NAME")
    COLLECTION = os.environ.get("COLLECTION")
