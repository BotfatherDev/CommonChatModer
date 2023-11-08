"""Тут находятся рофлян хендлеры.
Не воспринимайте их серьезно. Но
функции полезные, даже очень"""
import datetime
import random
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
    """Handler for the /gay command.
    In a humorous and respectful manner, the bot sends a random percentage reflecting a playful take on the user's alignment with a random LGBTQ+ orientation.

    Examples:
        /gay
        /gay Sam
    """
    # Reference the original message's author if it's a reply; otherwise, the command user.
    target = message.reply_to_message.from_user.get_mention(
        as_html=True) if message.reply_to_message else message.from_user.get_mention(
        as_html=True)

    percentage = randint(0, 100)

    # these are a little cringy but doesn't matter
    phrases = [
        "🌈 Виглядає, що сьогодні {username} на {percentage}% гей — жартуємо з любов'ю!",
        "🌈 Сьогодні {username} може бути {percentage}% лесбійка, святкуємо різноманітність!",
        "🌈 {username} виглядає на {percentage}% бісексуал сьогодні, які пригоди чекають?",
        "🌈 Сьогоднішній дух {username} - {percentage}% трансгендер, вітаємо усі кольори веселки!",
        "🌈 За шкалою квір-енергії {username} на {percentage}%, яскраво і гордо!",
        "🌈 Чи знаєте ви, що {username} сьогодні на {percentage}% асексуал? Розкриваємо таємниці!",
        "🌈 Пансексуальні вібрації {username} сягають {percentage}% сьогодні, хай буде весело!",
        "🌈 {username} сьогодні випромінює небінарну енергію на {percentage}%, унікально і стильно!",
        "🌈 Гей-радар показує, що {username} на {percentage}% гей сьогодні, час для райдужних святкувань!",
        "🌈 Магічний квір-кубик вирішив, що {username} сьогодні {percentage}% лесбійка, неймовірно та яскраво!"
    ]

    # Send the result with a random orientation
    await message.reply(random.choice(phrases).format(username=target, percentage=percentage))



def determine_gender(name):
    # Lists of explicit names
    man_names = ['Міша', 'Bodya']
    woman_names = ['Настенька']

    # Women name endings
    women_name_endings = '|'.join([
        'sa', 'са', 'ta', 'та', 'ша', 'sha', 'на', 'na', 'ия', 'ia',  # existing
        'va', 'ва', 'ya', 'я', 'ina', 'ина', 'ka', 'ка', 'la', 'ла',  # Slavic languages
        'ra', 'ра', 'sia', 'сия', 'ga', 'га', 'da', 'да', 'nia', 'ния', # Slavic languages
        'lie', 'ly', 'lee', 'ley', 'la', 'le', 'ette', 'elle', 'anne'  # English language
    ])

    # Check explicit list and name suffixes
    if name in woman_names or re.search(f'\w*({women_name_endings})(\W|$)', name, re.IGNORECASE):
        return 'woman'
    else:
        return 'man'

def select_emoji(length, is_biba):
    # Emojis for bibas, from smallest to largest
    biba_emojis = ['🥒', '🍌', '🌽', '🥖', '🌵', '🌴']

    # Emojis for breasts, from smallest to largest
    breast_emojis = ['🍓', '🍊', '🍎', '🥭', '🍉', '🎃']

    # Select the appropriate list of emojis
    emojis = biba_emojis if is_biba else breast_emojis

    # Select an emoji based on length
    for size, emoji in zip((1, 5, 10, 15, 20, 25), emojis):
        if length <= size:
            return emoji

    # If none of the sizes matched, return the largest emoji
    return emojis[-1]


@rate_limit(60, "fun")
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
    
    gender = determine_gender(message.from_user.first_name)

    # Random chance to switch gender
    switch_chance = 20 if gender == 'woman' else 40
    if random.randint(1, 100) <= switch_chance:
        gender = 'man' if gender == 'woman' else 'woman'

    # Select an emoji for the biba or breast
    is_biba = (gender == 'man')
    emoji = select_emoji(length, is_biba)

    # Send message based on final gender
    if gender == 'woman':
        await message.reply(f'{emoji} У {target} грудь {length // 5} размера.')
    else:
        # replace with your message for men
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
