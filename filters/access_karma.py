from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from data.cache_karma import reply_message_id_user
from loader import db, bot


class Restriction_Karma(BoundFilter):

    async def check(self, message: types.Message) -> bool:
        bot_id = (await bot.get_me()).id
        my_user_id = message.from_user.id
        user_id_not_karma = [bot_id, my_user_id]

        # чтобы нельзя было давать карму боту и самому себе
        if message.reply_to_message.from_user.id in user_id_not_karma:
            await message.delete()
            return False

        if await self._get_cached_message_value(message) is None:
            await self._set_cached_message_value(message)
            db.add_user(user_id=message.reply_to_message.from_user.id,
                        full_name=message.reply_to_message.from_user.full_name)
            await message.delete()
            return True

    async def _set_cached_message_value(self, message: types.Message):
        if not await self._get_cached_message_value(message) is None:
            return
        reply_message_id_user[message.reply_to_message.message_id] = message.from_user.id

    async def _get_cached_message_value(self, message: types.Message):
        try:
            return reply_message_id_user[message.reply_to_message.message_id]
        except Exception as error:
            logger.info(error)





