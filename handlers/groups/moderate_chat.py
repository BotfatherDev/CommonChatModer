import asyncio
import datetime
import re

import aiogram
from aiogram import types
from aiogram.utils.exceptions import BadRequest

from loader import bot, dp
from aiogram.dispatcher.filters import Command, AdminFilter
from filters import IsGroup

import logging


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["ro"], prefixes="!/"))
async def read_only_mode(message: types.Message):

    """
    Хендлер с фильтром в группе, где можно использовать команду !ro ИЛИ /ro

    :time int: время на которое нужно замутить пользователя в минутах
    :reason str: причина мута

    Примеры:

    Простейший мут на 10 минут:
        !ro 10
        или
        /ro 10

    Мут на 50 минут с причиной мута:
        !ro 50 читай мануал
        или
        /ro 50 читай мануал

    Мут на стандартные 5 минут:
        !ro спам
        или
        /ro спам
    """
    # разбиваем комманду на аргументы, через регулярку
    member = message.reply_to_message.from_user.id
    chat = message.chat.id

    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([a-zA-Z ]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5

    """
    !ro 
    !ro 5 
    !ro 5 test
    !ro test
    !ro test test test
    /ro 
    /ro 5 
    /ro 5 test
    /ro test
    """

    # Получаем конечную дату, до которой нужно забанить
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(time))

    try:
        # Пытаемся забрать права у пользователя
        await message.chat.restrict(user_id=member, can_send_messages=False, until_date=until_date)
        await message.answer(
            f"Пользователю {message.reply_to_message.from_user.full_name} запрещено писать {time} минут.\n"
            f"По причине: \n<b>{comment}</b>"
        )
        # Вносим информацию о муте в лог
        logging.info(
            f"Пользователью @{message.reply_to_message.from_user.full_name} запрещено писать сообщения до {until_date}"
        )
        service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")
        # Если удалось успешно замутить пользователя, ждём 5 секунд
        await asyncio.sleep(5)
        # а после удаляем сообщение, на которое ссылался администратор, при муте
        await message.reply_to_message.delete()

    # Если бот не может забанить пользователя (администратора), возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest:
        service_message = await message.answer(
            "Пользователь является администратором чата, я не могу выдать ему RO\n"
            "Сообщение самоуничтожится через 5 секунд.",
            reply=True
        )
        # Вносим информацию о муте в лог
        logging.info(
            f"Бот не смог замутить пользователя @{message.reply_to_message.from_user.full_name}"
        )
        await asyncio.sleep(5)
        # Опять ждём перед выполнением следующего блока
    finally:
        # после прошедших 5 секунд, бот удаляет сообщение от администратора и от самого бота
        await message.delete()
        await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["unro"], prefixes="!/"))
async def undo_read_only_mode(message: types.Message):
    member = message.reply_to_message.from_user.id
    chat = message.chat.id
    
    await bot.restrict_chat_member(
        chat_id=chat, user_id=member,
        can_send_messages=True,
        can_add_web_page_previews=True,
        can_send_media_messages=True,
        can_send_other_messages=True
    )
    await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} был разбанен")

    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")
    # Пауза 5 сек
    await asyncio.sleep(5)

    # Удаляем сообщения
    # Вариант 1 - по API
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    # Вариант 2 - сокращенный
    await message.delete()
    await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["ban"], prefixes="!/"))
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user.id
    await message.chat.kick(user_id=member)

    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")
    # Пауза 5 сек
    await asyncio.sleep(5)

    # Удаляем сообщения
    await message.delete()
    await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["unban"], prefixes="!/"))
async def ban_user(message: types.Message):
    member = message.reply_to_message.from_user.id
    await message.chat.unban(user_id=member)

    # Пишем в чат
    await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} был разбанен")
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

    # Пауза 5 сек
    await asyncio.sleep(5)

    # Удаляем сообщения
    await message.delete()
    await service_message.delete()
