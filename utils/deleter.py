from contextlib import suppress
from typing import List

from aiogram.types import Message
from aiogram.utils.exceptions import MessageCantBeDeleted


async def delete_messages(*messages: Message):
    for message in messages:
        with suppress(MessageCantBeDeleted):
            await message.delete()
