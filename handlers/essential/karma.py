import re

from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter
from aiogram.utils.markdown import hlink, hbold

from data.cache_karma import reply_message_id_user
from data.config import ADMINS_ID
from filters import IsGroup, IsReplyFilter, IsPrivate, IsPrivateAdmin
from filters.access_karma import Restriction_Karma
from loader import dp, bot, db
from utils.misc import rate_limit
from utils.misc.karma import karma, url


@dp.message_handler(IsPrivate(), IsPrivateAdmin(ADMINS_ID), Command("clear"))
async def clear_cache_message_id_karma(message: types.Message):
    size = None

    if type(reply_message_id_user) is dict:
        size = 144
        if len(reply_message_id_user) > 8:
            size += 12 * (len(reply_message_id_user) - 8)
    await message.answer(f"Памяти в кэше {size}\n"
                         "Было очищено")
    reply_message_id_user.clear()

@rate_limit(limit=0)
@dp.message_handler(IsGroup(), Command("top_karma", prefixes="!/"))
async def result_top_users(message: types.Message):
    name_bot = await bot.get_me()
    command_parse = re.compile(r"(!top_karma|/top_karma) ?(\d+)?")
    a = command_parse.match(message.text)
    limit = a.group(2)

    if limit is None:
        limit = 10

    if int(limit) > 20:
        limit = 20

    list_top_users = db.select_karma_top(limit=limit)
    text_messages = [f"Топ участников чата по карме: {hbold(name_bot.full_name)}"]

    for count, user_object in enumerate(list_top_users, 1):
        user_id, karma_user, full_name = user_object
        text = f"{count}. {hlink(full_name, url(user_id))} - {karma_user} 💋"
        text_messages.append(text)

    await message.answer("\n".join(text_messages))

@rate_limit(limit=60)
@dp.message_handler(IsGroup(), IsReplyFilter(is_reply=True), Restriction_Karma(), text=["+", "-"])
async def give_karma_user(message: types.Message):

    answer = message.text
    text_with_karma = {"+": (1, "пополнил"),
                       "-": (-1, "понизил")}
    karma(message, karma=text_with_karma[f"{answer}"][0])

    user = hlink(message.from_user.first_name, message.from_user.url)
    text = text_with_karma.get(answer)[1]
    to_user = hlink(message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.url)
    get_karma = str(text_with_karma.get(answer)[0])
    total_karma = db.select_karma_user(user_id=message.reply_to_message.from_user.id)[0][1]  # получаем общую карму пользователя

    await message.answer(R"""{user} {text} {to_user} карму на {get_karma}
Текущая карма: {total_karma}""".format(user=user,
                                       text=text,
                                       to_user=to_user,
                                       get_karma=get_karma,
                                       total_karma=total_karma))
