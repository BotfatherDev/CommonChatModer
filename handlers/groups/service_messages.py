from aiogram import types

from loader import dp, bot
from filters import IsGroup


@dp.message_handler(IsGroup(), content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    await message.reply(f"Привет, {message.new_chat_members[0].full_name}.")


@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def banned_member(message: types.Message):
    await message.answer(f"{message.left_chat_member.full_name} был удален из чата "
                         f"пользователем {message.from_user.full_name}.")
