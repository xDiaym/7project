import logging
import os
from typing import Optional

from dotenv import load_dotenv
from vkbottle.bot import Bot, Message

from src.homework_storage.mongo import HomeworkStorage

load_dotenv()

storage = HomeworkStorage(
    os.environ.get("DB_NAME"),
    os.environ.get("COLLECTION")
)
bot = Bot(os.environ.get("BOT_TOKEN"))

logging.basicConfig(level=logging.INFO)


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


if __name__ == "__main__":
    bot.run_forever()
