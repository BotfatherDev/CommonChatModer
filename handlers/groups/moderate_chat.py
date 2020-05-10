import asyncio
import datetime
import re

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

    Самый простейший мут без аргументов:
    .. отвечаем на сообщение от пользователя с текстом
        !ro
        или
        /ro

    Мут на 10 минут:
    .. отвечаем на сообщение от пользователя с текстом
        !ro 10
        или
        /ro 10

    Мут на 50 минут с причиной мута:
    .. отвечаем на сообщение от пользователя с текстом
        !ro 50 читай мануал
        или
        /ro 50 читай мануал

    Мут на стандартные 5 минут:
    .. отвечаем на сообщение от пользователя с текстом
        !ro спам
        или
        /ro спам
    """
    # разбиваем комманду на аргументы, через регулярку
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([a-zA-Z ]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    comment = parsed.group(3)
    if not time:
        time = 5

    member = message.reply_to_message.from_user.id

    # Получаем конечную дату, до которой нужно забанить
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(time))

    try:
        # Пытаемся забрать права у пользователя
        await message.chat.restrict(user_id=member, can_send_messages=False, until_date=until_date)

        # Готовим сообщение, перед отправкой в чат
        answer_text = str(
            f"Пользователю {message.reply_to_message.from_user.get_mention(as_html=True)}"
            f" запрещено писать {time} минут.\n"
        )
        # Если добавлена причина, добавляем её и в сообщение перед ответом
        if comment:
            answer_text += f"По причине: \n<b>{comment}</b>"
        await message.answer(
            answer_text
        )
        # Вносим информацию о муте в лог
        logging.info(
            f"Пользователью @{message.reply_to_message.from_user.username} запрещено писать сообщения до {until_date}"
        )
        service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")
        # Если удалось успешно замутить пользователя, ждём 5 секунд
        await asyncio.sleep(5)
        # а после удаляем сообщение, на которое ссылался администратор, при муте
        await message.reply_to_message.delete()

    # Если бот не может замутить пользователя (администратора), возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest:
        service_message = await message.answer(
            f"Пользователь {message.reply_to_message.from_user.get_mention(as_html=True)} "
            "является администратором чата, я не могу выдать ему RO\n"
            "Сообщение самоуничтожится через 5 секунд.",
            reply=True
        )
        # Вносим информацию о муте в лог
        logging.info(
            f"Бот не смог замутить пользователя @{message.reply_to_message.from_user.username}"
        )
        await asyncio.sleep(5)
        # Опять ждём перед выполнением следующего блока
    finally:
        # после прошедших 5 секунд, бот удаляет сообщение от администратора и от самого бота
        await message.delete()
        await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["unro"], prefixes="!/"))
async def undo_read_only_mode(message: types.Message):
    """
    Хендлер с фильтром в группе, где можно использовать команду !unro ИЛИ /unro

    Примеры:

    Размут пользователя:

    .. отвечаем на сообщение от пользователя с текстом
        !unro
        или
        /unro
    """

    # Получаем айди чата и пользователя, для дальнейшего использования
    member = message.reply_to_message.from_user.id
    chat = message.chat.id

    # Возвращаем пользователю возможность отправлять сообщения и всё из этого вытекающее
    await bot.restrict_chat_member(
        chat_id=chat,
        user_id=member,
        can_send_messages=True,
        can_add_web_page_previews=True,
        can_send_media_messages=True,
        can_send_other_messages=True
    )

    # Информируем об этом
    await message.answer(f"Пользователь {message.reply_to_message.from_user.get_mention(as_html=True)} был размучен")
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

    # Не забываем про лог
    logging.info(
        f"Пользователь @{message.reply_to_message.from_user.username} был размучен"
    )

    # Пауза 5 сек
    await asyncio.sleep(5)

    # Удаляем сообщения от бота и администратора
    await message.delete()
    await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["ban"], prefixes="!/"))
async def ban_user(message: types.Message):
    """
    Хендлер с фильтром в группе, где можно использовать команду !ban ИЛИ /ban

    Примеры:

    Бан пользователя:

    .. отвечаем на сообщение от пользователя с текстом
        !ban
        или
        /ban
    """

    # Получаем айди пользователя
    member = message.reply_to_message.from_user.id

    try:
        # Пытаемся удалить пользователя из чата
        await message.chat.kick(user_id=member)

        # Информируем об этом
        await message.answer(
            f"Пользователь {message.reply_to_message.from_user.get_mention(as_html=True)} был успешно забанен"
        )
        # Об успешном бане информируем разработчиков в лог
        logging.info(
            f"Бот успешно забанил пользователя @{message.reply_to_message.from_user.username}"
        )
        service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

        # После чего засыпаем на 5 секунд
        await asyncio.sleep(5)

        # Не забываем удалить сообщение, на которое ссылался администратор
        await message.reply_to_message.delete()

    # Если бот не может забанить пользователя (администратора), возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest as err:
        service_message = await message.answer(
            f"Пользователь {message.reply_to_message.from_user.get_mention(as_html=True)} "
            "является администратором чата, я не могу забанить его\n"
            "Сообщение самоуничтожится через 5 секунд.",
            reply=True
        )
        # Вносим информацию о муте в лог
        logging.info(
            f"Бот не смог забанить пользователя @{message.reply_to_message.from_user.username}"
        )
        # После чего засыпаем на 5 секунд
        await asyncio.sleep(5)

    # В случае любой другой ошибки, пишем её в лог, для последующего деббага
    except Exception as err:
        logging.exception(err)

    finally:
        # В итоге удаляем сообщения
        await message.delete()
        await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["unban"], prefixes="!/"))
async def ban_user(message: types.Message):
    """
    Хендлер с фильтром в группе, где можно использовать команду !unban ИЛИ /unban

    Примеры:

    Разбан пользователя:

    .. отвечаем на сообщение от пользователя с текстом
        !unban
        или
        /unban
    """

    # Получаем айди пользователя
    member = message.reply_to_message.from_user.id

    # И разбаниваем
    await message.chat.unban(user_id=member)

    # Пишем в чат
    await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} был разбанен")
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

    # Пауза 5 сек
    await asyncio.sleep(5)

    # Удаляем сообщения
    await message.delete()
    await service_message.delete()
