from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import bot


class IsContributor(BoundFilter):

    async def check(self, message: types.Message):
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return member.custom_title == "Contributor"
