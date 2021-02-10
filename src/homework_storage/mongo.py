from typing import Optional

import motor.motor_asyncio

from src.homework_storage.abstract_storage import ABCHomeworkStorage


class HomeworkStorage(ABCHomeworkStorage):
    def __init__(self, table: str, collection: str, *args, **kwargs) -> None:
        client = motor.motor_asyncio.AsyncIOMotorClient(*args, **kwargs)
        self._collection = client[table][collection]

    async def set_homework(
        self, group_id: int, lesson: str, homework: str
    ) -> None:
        lesson = lesson.lower()
        await self._collection.find_one_and_update(
            {"group_id": group_id, "lesson": lesson},
            {
                "$set": {
                    "group_id": group_id,
                    "lesson": lesson,
                    "homework": homework,
                }
            },
            upsert=True,
        )

    async def get_homework(self, group_id: int, lesson: str) -> Optional[str]:
        record = await self._collection.find_one(
            {"group_id": group_id, "lesson": lesson.lower()}
        )
        return record["homework"] if record is not None else None
