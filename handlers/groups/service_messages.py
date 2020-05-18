import asyncio
import datetime

from aiogram import types

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def left_chat_member(message: types.Message):
    """Хендлер для вышедших либо кикнутых пользователей"""

    # TODO: Можно дёрнуть getChatMember на этот ID. Вернётся тип ChatMember с полем status.
    #  Это поле может принимать разные, значения, есть отдельно left, отдельно kicked
    #  А left_chat_member в Message в какой-то момент перестанет появляться вообще
    #  (спасибо челу из чата аиограма)

    # Пропускаем старые запросы
    if message.date < datetime.datetime.now() - datetime.timedelta(minutes=1):
        return False

    # Если пользователя удалил бот, то это было сделано через /ban - пропускаем
    bot = await message.bot.get_me()
    elif message.from_user.id == bot.id:
        return False

    # Проверяем вышел ли пользователь сам
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} вышел из чата.")

    else:
        await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} был удален из чата "
                             f"пользователем {message.from_user.get_mention(as_html=True)}.")


@dp.message_handler(IsGroup(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    # Пропускаем старые запросы
    if message.date < datetime.datetime.now() - datetime.timedelta(minutes=1):
        return False

    # Делаем приветствие для новых пользователей
    # TODO: сделать проверку на ботов с помощью инлайн кнопок

    users = {}
    for new_member in message.new_chat_members:
        users[new_member.id] = new_member.get_mention()

    await message.reply(
        (
            "{users}, добро пожаловать в чат!"
        ).format(users=", ".join(users.values()))
    )
