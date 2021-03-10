import logging

from vkbottle.bot import Bot

from config import BotConfig
from sevenproject.help import bp as help_bp
from sevenproject.homework import bp as homework_bp

logging.basicConfig(level=logging.DEBUG)


def create_bot() -> Bot:
    bot = Bot(BotConfig.TOKEN)
    homework_bp.load(bot)
    help_bp.load(bot)
    return bot
