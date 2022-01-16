import asyncio
import random

from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.types import Message, Chat
from async_lru import alru_cache

from filters import IsGroup
from loader import db, dp, bot

from utils.misc.rating import caching_rating, get_rating


@dp.message_handler(
    IsGroup(),
    IsReplyFilter(True),
    text=["+", "-"])
async def add_rating_handler(m: Message):
    helper_id = m.reply_to_message.from_user.id  # айди хелпера
    user_id = m.from_user.id  # айди, который поставил + или -
    message_id = m.reply_to_message.message_id

    if m.bot.id == helper_id or user_id == helper_id:
        return await m.delete()

    cached = caching_rating(m, helper_id, user_id, message_id)
    if cached == "flood":
        return await m.delete()

    if not cached:
        return await m.delete()

    ratings = {
        "+": 1,
        "-": -1
    }
    rating_user = get_rating(helper_id, ratings.get(m.text))

    if m.text == "+":
        text = f"{m.from_user.mention} <b>повысил рейтинг на 1 пользователю</b> {m.reply_to_message.from_user.mention}😳\n" \
               f"<b>Текущий рейтинг: {rating_user}</b>"
    else:
        text = f"{m.from_user.mention} <b>понизил рейтинг на 1 пользователю</b> {m.reply_to_message.from_user.mention}\n 😳" \
               f"<b>Текущий рейтинг: {rating_user}</b>"

    await m.answer(text)


@alru_cache(maxsize=10)
async def get_profile(user_id) -> Chat:
    await asyncio.sleep(0.1)
    chat = await bot.get_chat(user_id)
    return chat.full_name


@dp.message_handler(commands=['top_helpers'])
async def get_top_helpers(m: Message):
    helpers = db.get_top_by_rating()
    emoji_for_top = [
        "🐤", "🐙", "🐮", "🐻", "🐼", "🐸", "🐰", "🦊", "🦁", "🙈", "🦕"
    ]
    random.shuffle(emoji_for_top)

    text = """
Топ Хелперов:
{tops}
""".format(
        tops="\n".join([

            f"<b>{emoji_for_top[number]} {await get_profile(helper[0])} - {helper[1]}</b> " for number, helper in
            enumerate(helpers, 0)]
        )
    )
    await m.answer(text)
