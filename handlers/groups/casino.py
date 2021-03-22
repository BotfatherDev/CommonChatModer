import asyncio
import datetime

from aiogram import types
from aiogram.utils.exceptions import BadRequest
from loguru import logger

from data.permissions import set_user_ro_permissions
from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), content_types=types.ContentType.DICE)
async def win_or_loss(message: types.Message):
    if message.dice.emoji != "🎰":
        return

    value = message.dice.value
    slots = {
        1: {"values": ("bar", "bar", "bar"), "time": 10, "prize": "3X BAR"},
        22: {"values": ("grape", "grape", "grape"), "time": 15, "prize": "🍇🍇🍇"},
        43: {"values": ("lemon", "lemon", "lemon"), "time": 20, "prize": "🍋🍋🍋"},
        64: {"values": ("seven", "seven", "seven"), "time": 25, "prize": "🔥JACKPOT🔥"},
    }

    if value not in slots:
        await asyncio.sleep(2.35)
        return await message.delete()

    time = slots[value]["time"]
    prize = slots[value]["prize"]

    if message.forward_from:
        time += time
        prize += " а так же жульничал"

    until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(time))
    username = message.from_user.username
    name = message.from_user.get_mention(as_html=True)

    try:
        await asyncio.sleep(1.67)
        await message.chat.restrict(
            user_id=message.from_user.id,
            permissions=set_user_ro_permissions(),
            until_date=until_date,
        )

        await message.answer(
            f"Пользователь {name} "
            f"выбил {prize} и получил "
            f"RO на {time} минут.\n"
            f"Поздравляем!"
        )

    except BadRequest:
        await message.answer(
            f"Администратор чата {name} выиграл в казино {prize}"
        )

        logger.info(
            f"Бот не смог замутить пользователя @{username} ({name})"
            f"по причине: выиграл в казино"
        )
    else:
        logger.info(
            f"Пользователю @{username} ({name}) запрещено писать сообщения до {until_date} "
            f"по причине: выиграл в казино"
        )
