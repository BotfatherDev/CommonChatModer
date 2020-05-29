from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import bot


class IsBanable(BoundFilter):

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.can_restrict_members
