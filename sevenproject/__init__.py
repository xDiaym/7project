import logging

from vkbottle.bot import Bot

from config import BotConfig
from sevenproject.blueprints.ban import bp as ban_bp
from sevenproject.blueprints.help import bp as help_bp
from sevenproject.blueprints.homework import bp as homework_bp

logging.basicConfig(level=logging.DEBUG)

BLUEPRINTS = (help_bp, homework_bp, ban_bp)


def create_bot() -> Bot:
    bot = Bot(BotConfig.TOKEN)
    for bp in BLUEPRINTS:
        bp.load(bot)
    return bot
