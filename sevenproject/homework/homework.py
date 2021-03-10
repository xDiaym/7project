from typing import Optional

from vkbottle.bot import Blueprint, Message

from config import DatabaseConfig
from sevenproject.homework.homework_storage.mongo import HomeworkStorage

bp = Blueprint()
storage = HomeworkStorage(DatabaseConfig.NAME, DatabaseConfig.COLLECTION)


@bp.on.chat_message(
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


@bp.on.chat_message(text=["/задание <lesson>", "/задание"])
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
