import asyncio
import datetime

from aiogram.utils.exceptions import BadRequest
from aiogram import types
from loguru import logger

from data.permissions import set_user_ro_permissions
from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), content_types=types.ContentType.DICE)
async def win_or_loss(message: types.Message):
    if message.dice.emoji != '🎰':
        return

    value = message.dice.value
    slots = {
        1: ("bar", "bar", "bar"),
        22: ("grape", "grape", "grape"),
        43: ("lemon", "lemon", "lemon"),
        64: ("seven", "seven", "seven"),
    }

    for i in slots:
        if value == i:
            if i == 1:
                time = 10
                prize = "3X BAR"
            elif i == 22:
                time = 15
                prize = "🍇🍇🍇"
            elif i == 43:
                time = 20
                prize = "🍋🍋🍋"
            else:
                time = 25
                prize = "🔥JACKPOT🔥"

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
                print(set_user_ro_permissions())

                await message.answer(
                    f"Пользователь {name} "
                    f"выбил {prize} и получил "
                    f"RO на {time} минут.\n"
                    f"Поздравляем!")
            except BadRequest:
                await message.answer(
                    f"Администратор чата {name} "
                    f"выиграл в казино {prize}"
                )

                logger.info(f"Бот не смог замутить пользователя @{username} ({name})"
                            f"по причине: выиграл в казино")
            else:
                logger.info(
                    f"Пользователю @{username} ({name}) запрещено писать сообщения до {until_date} "
                    f"по причине: выиграл в казино"
                )
                break
        else:
            pass
    else:
        await asyncio.sleep(3)
        await message.delete()



