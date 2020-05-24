import datetime
import re

import asyncio
from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter
from aiogram.utils.exceptions import BadRequest
from loguru import logger

from filters import IsGroup
from loader import bot, dp

from data.permissions import user_ro, user_allowed


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["ro"], prefixes="!/"))
async def read_only_mode(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !ro ИЛИ /ro
    :time int: время на которое нужно замутить пользователя в минутах
    :reason str: причина мута. При отсуствии времени и/или причины, то
    используються стандартные значения: 5 минут и None для времени и причины соответсвенно"""

    # Создаем переменные для удобства
    admin_username = message.from_user.username
    admin_mentioned = message.from_user.get_mention(as_html=True)

    # Пробуем присвоить значения пересланного пользователя
    try:
        member_id = message.reply_to_message.from_user.id
        member_username = message.reply_to_message.from_user.username
        member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)

    # Ловим ошибку, если пользователь не переслал сообщение
    except AttributeError:
        await message.reply("Ошибка. Нужно переслать сообщение")
        return False

    # Разбиваем команду на аргументы с помощью RegExp
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)
    reason = parsed.group(3)
    # Проверяем на наличие и корректность срока RO
    if not time:
        time = 5
    else:
        if int(time) < 1:
            time = 1
    # Проверяем на наличие причины
    if not reason:
        reason = "без указания причины"
    else:
        reason = "по причине: " + reason
    # Получаем конечную дату, до которой нужно замутить
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(time))

    try:

        # Пытаемся забрать права у пользователя
        await message.chat.restrict(
            user_id=member_id,
            permissions=user_ro,
            until_date=until_date)

        # Отправляем сообщение
        await message.answer(
            f"Пользователю {member_mentioned} "
            f"было запрещено писать на {time} минут "
            f"администратором {admin_mentioned} {reason} ")

        # Вносим информацию о муте в лог
        logger.info(
            f"Пользователю @{member_username} запрещено писать сообщения до {until_date} админом @{admin_username}"
        )

        service_message = await message.reply("Сообщение самоуничтожится через 5 секунд")
        await asyncio.sleep(5)
        await message.reply_to_message.delete()

    # Если бот не может замутить пользователя (администратора), возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest:

        # Отправляем сообщение
        await message.answer(
            f"Пользователь {member_mentioned} "
            "является администратором чата, я не могу выдать ему RO"
        )

        service_message = await message.reply(f"Сообщение самоуничтожится через 5 секунд.")

        # Вносим информацию о муте в лог
        logger.info(f"Бот не смог замутить пользователя @{member_username}")

        # Опять ждём перед выполнением следующего блока
        await asyncio.sleep(5)

    # В случае любой другой ошибки, пишем её в лог, для последующего деббага
    except Exception as err:
        logger.exception(err)
    finally:
        # после прошедших 5 секунд, бот удаляет сообщение от администратора и от самого бота
        await message.delete()
        await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["unro"], prefixes="!/"))
async def undo_read_only_mode(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !unro ИЛИ /unro"""

    # Создаем переменные для удобства
    admin_username = message.from_user.username
    admin_mentioned = message.from_user.get_mention(as_html=True)
    chat_id = message.chat.id

    # Пробуем присвоить значения пересланного пользователя
    try:
        member_id = message.reply_to_message.from_user.id
        member_username = message.reply_to_message.from_user.username
        member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)

    # Ловим ошибку, если пользователь не переслал сообщение
    except AttributeError:
        await message.reply("Ошибка. Нужно переслать сообщение")
        return False

    # Возвращаем пользователю возможность отправлять сообщения
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=member_id,
        permissions=user_allowed,
    )

    # Информируем об этом
    await message.answer(f"Пользователь {member_mentioned} был размучен администратором {admin_mentioned}")
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

    # Не забываем про лог
    logger.info(
        f"Пользователь @{member_username} был размучен администратором @{admin_username}"
    )

    # Пауза 5 сек
    await asyncio.sleep(5)

    # Удаляем сообщения от бота и администратора
    await message.delete()
    await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["ban"], prefixes="!/"))
async def ban_user(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !ban ИЛИ /ban"""

    # Создаем переменные для удобства
    admin_fullname = message.from_user.full_name
    admin_mentioned = message.from_user.get_mention(as_html=True)

    # Пробуем присвоить значения пересланного пользователя
    try:
        member_id = message.reply_to_message.from_user.id
        member_fullname = message.reply_to_message.from_user.full_name
        member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)

    # Ловим ошибку, если пользователь не переслал сообщение
    except AttributeError:
        await message.reply("Ошибка. Нужно переслать сообщение")
        return False

    try:
        # Пытаемся удалить пользователя из чата
        await message.chat.kick(user_id=member_id)

        # Информируем об этом
        await message.answer(
            f"Пользователь {member_mentioned} был успешно забанен администратором {admin_mentioned}"
        )
        # Об успешном бане информируем разработчиков в лог
        logger.info(
            f"Пользователь {member_fullname} был забанен админом {admin_fullname}"
        )
        service_message = await message.answer("Сообщение самоуничтожится через 5 секунд.")

        # После чего засыпаем на 5 секунд
        await asyncio.sleep(5)

        # Не забываем удалить сообщение, на которое ссылался администратор
        await message.reply_to_message.delete()

    # Если бот не может забанить пользователя (администратора), возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest:

        # Отправляем сообщение
        await message.answer(
            f"Пользователь {member_mentioned} "
            "является администратором чата, я не могу выдать ему RO"
        )

        service_message = await message.answer(f"Сообщение самоуничтожится через 5 секунд.", reply=False)

        # Вносим информацию о бане в лог
        logger.info(f"Бот не смог забанить пользователя {member_fullname}")

        # После чего засыпаем на 5 секунд
        await asyncio.sleep(5)

    # В случае любой другой ошибки, пишем её в лог, для последующего деббага
    except Exception as err:
        logger.exception(err)
    finally:
        # В итоге удаляем сообщения
        await message.delete()
        await service_message.delete()


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["unban"], prefixes="!/"))
async def unban_user(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !unban ИЛИ /unban"""

    # Создаем переменные для удобства
    admin_username = message.from_user.username
    admin_mentioned = message.from_user.get_mention(as_html=True)

    # Пробуем присвоить значения пересланного пользователя
    try:
        member_id = message.reply_to_message.from_user.id
        member_username = message.reply_to_message.from_user.username
        member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)

    # Ловим ошибку, если пользователь не переслал сообщение
    except AttributeError:
        await message.reply("Ошибка. Нужно переслать сообщение")
        return False

    # И разбаниваем
    await message.chat.unban(user_id=member_id)

    # Пишем в чат
    await message.answer(f"Пользователь {member_mentioned} был разбанен администратором {admin_mentioned}")
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

    # Пауза 5 сек
    await asyncio.sleep(5)

    # Записываем в логи
    logger.info(
        f"Пользователь @{member_username} был забанен админом @{admin_username}"
    )

    # Удаляем сообщения
    await message.delete()
    await service_message.delete()
