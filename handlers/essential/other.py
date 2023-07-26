"""Тут находяться рофлян хендлеры.
Не воспринимайте их серьезно. Но
функции полезные, даже очень"""
import datetime
import re
from random import randint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.permissions import set_user_ro_permissions
from loader import db
from utils.misc import rate_limit
from utils.misc.random_num_generator import generate_num


@rate_limit(120, "gay")
async def gay(message: types.Message):
    """Хедлер, для обработки комманды /gay или !gay
    В ответ, бот отправляет то, на сколько пользователь является геем

    Примеры:
        /gay
        /gay Vasya
        !gay
        !gay Vasya
    """
    # если это ответ на сообщение, будем берять бибу автора первичного сообщения
    # в противном случае, бибу того, кто использовал комманду
    if message.reply_to_message:
        target = message.reply_to_message.from_user.get_mention(as_html=True)
    else:
        target = message.from_user.get_mention(as_html=True)

    percentage = randint(0, 100)

    # отправляем результат
    await message.reply(f"🏳️‍🌈 Похоже, что {target} гей на {percentage}%")


@rate_limit(120, "fun")
async def biba(message: types.Message):
    """Хедлер, для обработки комманды /biba или !biba

    В ответ, бот отправляет размер бибы

    Примеры:
        /biba
        /biba 10
        /biba 1-10
        /biba 10-1
        !biba
        !biba 10
        !biba 1-10
        !biba 10-1
    """
    # разбиваем сообщение на комманду и аргументы через регулярное выражение
    command_parse = re.compile(r"(!biba|/biba) ?(-?\d*)?-?(\d+)?")
    parsed = command_parse.match(message.text)
    # генерируем размер бибы от 1 до 30 по умолчанию (если аргументы не переданы)
    length = generate_num(parsed.group(2), parsed.group(3), 1, 30)

    # если это ответ на сообщение, будем берять бибу автора первичного сообщения
    # в противном случае, бибу того, кто использовал комманду
    if message.reply_to_message:
        target = message.reply_to_message.from_user.get_mention(as_html=True)
    else:
        target = message.from_user.get_mention(as_html=True)
    women_name_endings = '|'.join([
    'sa', 'са', 'ta', 'та', 'ша', 'sha', 'на', 'na', 'ия', 'ia',  # existing
    'va', 'ва', 'ya', 'я', 'ina', 'ина', 'ka', 'ка', 'la', 'ла',  # Slavic languages
    'ra', 'ра', 'sia', 'сия', 'ga', 'га', 'da', 'да', 'nia', 'ния', # Slavic languages
    'lie', 'ly', 'lee', 'ley', 'la', 'le', 'ette', 'elle', 'anne'  # English language
        ])
    if re.search(f'\w*({women_name_endings})\W', message.from_user.first_name, re.IGNORECASE): 
        await message.reply(f'У {target} грудь {length // 5} размера.')
        return
    # отправляем
    emojis = ['🥲', '😔', '😋', '😏', '🤤', '🥸']
    emoji = ''
    for size, selected_emoji in zip((1, 5, 10, 15, 20, 25), emojis):
        if length <= size:
            break

        emoji = selected_emoji

    await message.reply(f"{emoji} У {target} биба {length} см")


@rate_limit(10, "fun")
async def roll(message: types.Message):
    """Хедлер, для обработки комманды /roll или !roll

    В ответ, бот отправляет рандомное число

    Примеры:

        /roll
        /roll 10
        /roll 1-10
        /roll 10-1
        !roll
        !roll 10
        !roll 1-10
        !roll 10-1
    """
    # разбиваем сообщение на комманду и аргументы через регулярное выражение
    command_parse = re.compile(r"(!roll|/roll) ?(-?\d*)?-?(\d+)?")
    parsed = command_parse.match(message.text)
    # генерируем число
    num = generate_num(parsed.group(2), parsed.group(3))
    # отправляем число
    await message.reply(f"Ваше число: <b>{num}</b>")


async def delete_hamster(message: types.Message, state: FSMContext):
    sticker_sets = [set_name for (set_name,) in db.select_all_sets()]
    if message.sticker.set_name in sticker_sets:
        await message.delete()

        async with state.proxy() as data:
            if not data.get("Sticker Flood"):
                data["Sticker Flood"] = 1
            else:
                data["Sticker Flood"] += 1
                if data["Sticker Flood"] >= 3:
                    try:
                        await message.chat.restrict(
                            user_id=message.from_user.id,
                            permissions=set_user_ro_permissions(),
                            until_date=datetime.datetime.now()
                                       + datetime.timedelta(minutes=int(10)),
                        )
                    except Exception as err:
                        pass
                    await message.answer(
                        f"{message.from_user.get_mention(as_html=True)} забанен на 10 мин "
                        f"за плохие стикеры."
                    )

                    data["Sticker Flood"] = 0

                    # я обиделся

                    return
        await message.answer(
            f"{message.from_user.get_mention(as_html=True)}! Ща забаню сука."
        )


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(gay, Command("gay", prefixes="!/"))
    dp.register_message_handler(biba, Command("biba", prefixes="!/"))
    dp.register_message_handler(roll, Command("roll", prefixes="!/"))
    dp.register_message_handler(delete_hamster, content_types=types.ContentType.STICKER)
