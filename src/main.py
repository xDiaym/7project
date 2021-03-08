import logging
import os
from typing import Optional

from dotenv import load_dotenv
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.bot import FuncRule
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from vkbottle_types.objects import MessagesMessageActionStatus

from homework_storage.mongo import HomeworkStorage

load_dotenv()

BOT_ID = os.environ.get("BOT_ID")

storage = HomeworkStorage(
    os.environ.get("DB_NAME"), os.environ.get("COLLECTION")
)

bot = Bot(os.environ.get("BOT_TOKEN"))

logging.basicConfig(level=logging.DEBUG)


@bot.on.chat_message(
    text=["/добавить <lesson> <homework>", "/добавить <lesson>", "/добавить"]
)
async def set_homework(
    message: Message,
    lesson: Optional[str] = None,
    homework: Optional[str] = None,
) -> None:
    if lesson is None or homework is None:
        await message.answer("❌ Использование: /добавить <lesson> <homework>")
    else:
        await storage.set_homework(message.group_id, lesson, homework)
        await message.answer(
            f'Отлично! 👍 Я запомнил задание по предмету "{lesson}"'
        )


@bot.on.chat_message(text=["/задание <lesson>", "/задание"])
async def get_homework(message: Message, lesson: Optional[str] = None) -> None:
    if lesson is None:
        await message.answer(f"❌ Выбери предмет!")
    else:
        homework = await storage.get_homework(message.group_id, lesson)
        if homework is not None:
            await message.answer(
                f'✔️ Задание по предмету "{lesson.lower()}":\n{homework}'
            )
        else:
            await message.answer("❌ Не могу найти задание/предмет")


def has_bot_invited(message: MessageMin) -> bool:
    return (
        message and
        message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER
        and message.action.member_id == BOT_ID
    )


@bot.on.chat_message(text=["/помощь"])
@bot.on.chat_message(FuncRule(has_bot_invited))
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


if __name__ == "__main__":
    bot.run_forever()
