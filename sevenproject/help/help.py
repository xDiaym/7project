from vkbottle.bot import Message, Blueprint
from vkbottle.dispatch.rules.bot import FuncRule
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from vkbottle_types.objects import MessagesMessageActionStatus

from config import BotConfig

bp = Blueprint()


def has_bot_invited(message: MessageMin) -> bool:
    return (
        message.action
        and message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER
        and message.action.member_id == BotConfig.ID
    )


@bp.on.chat_message(text=["/помощь"])
@bp.on.chat_message(FuncRule(has_bot_invited))
async def help_(message: Message):
    await message.answer(
        "👋 Привет! Я - бот, и теперь буду помогать вам обмениваться "
        "домашним заданием.\n"
        "📚 Список моих команд:\n"
        "/добавить [предмет] [задание] - добавит задание по "
        "выбранному предмету\n"
        "/задание [предмет] - отправит задания по выбранному предмету\n"
        "/помощь - отправит это сообщение"
    )
