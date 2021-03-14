import motor.motor_asyncio

from sevenproject.storage.ban.abstract import ABCBanStorage


class BanStorage(ABCBanStorage):
    def __init__(self, table: str, collection: str = "ban", *args,
                 **kwargs) -> None:
        client = motor.motor_asyncio.AsyncIOMotorClient(*args, **kwargs)
        self._collection = client[table][collection]

    async def ban(self, group_id: int, user_id: int) -> None:
        await self._collection.insert_one({
            "group_id": group_id,
            "user_id": user_id
        })

    async def unban(self, group_id: int, user_id: int) -> None:
        await self._collection.delete_one({
            "$and": [{"group_id": group_id}, {"user_id": user_id}]
        })

    async def was_banned(self, group_id: int, user_id: int) -> bool:
        return bool(await self._collection.find_one({
            "$and": [{"group_id": group_id}, {"user_id": user_id}]
        }))
