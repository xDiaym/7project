import re
from typing import Optional

from vbml import Patcher
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.bot import VBMLRule

from sevenproject.storage.ban.mongo import BanStorage

bp = Blueprint()
db = BanStorage("7project")

patcher = Patcher()
MENTION_REGEX = re.compile(r"\[id(\d+)\|[@*].+]")


@patcher.validator("mention")
def mention_validator(value: str) -> int:
    group = re.findall(MENTION_REGEX, value)
    if group:
        return int(group[0])


async def is_admin(peer_id: int, user_id: int) -> bool:
    response = await bp.api.messages.get_conversation_members(peer_id)
    admins = filter(lambda x: x.is_admin or x.is_owner, response.items)
    return user_id in map(lambda x: x.member_id, admins)


@bp.on.chat_message(VBMLRule(['/бан', '/бан <user:mention>'], patcher))
async def ban(message: Message, user: Optional[int] = None) -> None:
    try:
        has_permission = await is_admin(message.peer_id, message.from_id)
    except:
        await message.answer("❌ У меня нет прав адинистратора!")
        return

    if user is None:
        await message.answer("❌ Вы не указали пользователя!")
    elif not has_permission:
        await message.answer("❌ Вы не админ!")
    else:
        await db.ban(message.group_id, user)
        await message.answer("Пользователь заблокирован!")


@bp.on.chat_message(VBMLRule(['/разбан', '/разбан <user:mention>'], patcher))
async def unban(message: Message, user: Optional[int] = None) -> None:
    try:
        has_permission = await is_admin(message.peer_id, message.from_id)
    except:
        await message.answer("❌ У меня нет прав адинистратора!")
        return

    if user is None:
        await message.answer("❌ Вы не указали пользователя")
    elif not has_permission:
        await message.answer("❌ Вы не админ!")
    else:
        await db.unban(message.group_id, user)
        await message.answer("Пользователь разблокирован!")
