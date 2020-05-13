import asyncio
import datetime
import re

from aiogram import types
from aiogram.dispatcher.filters import Command, AdminFilter
from aiogram.utils.exceptions import BadRequest
from loguru import logger

from filters import IsGroup
from loader import bot, dp


@dp.message_handler(IsGroup(), AdminFilter(), Command(commands=["ro"], prefixes="!/"))
async def read_only_mode(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !ro ИЛИ /ro
    :time int: время на которое нужно замутить пользователя в минутах
    :reason str: причина мута. При отсуствии времени и/или причины, то
    используються стандартные значения: 5 минут и None для времени и причины соответсвенно"""

    # Создаем переменные для удобства
    try:
        member_id = message.reply_to_message.from_user.id
        member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)
        admin_id = message.from_user.id
        admin_mentioned = message.from_user.get_mention(as_html=True)

    # Ловим ошибку, если пользователь не переслал сообщение
    except AttributeError:
        await message.reply("Ошибка. Нужно переслать сообщение")
        return False

    # Разбиваем команду на аргументы с помощью RegExp
    command_parse = re.compile(r"(!ro|/ro) ?(\d+)? ?(\w+)?")
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
        reason = "без причины"
    else:
        reason = "по причине: " + reason

    # Получаем конечную дату, до которой нужно замутить
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(time))

    try:

        # Пытаемся забрать права у пользователя
        await message.chat.restrict(
            user_id=member_id,
            can_send_messages=False,
            until_date=until_date)

        # Отправляем сообщение
        await message.reply(
            f"Пользователю {member_mentioned} "
            f"было запрещено писать на {time} минут "
            f"администратором {admin_mentioned} {reason} ", reply=False)

        # Вносим информацию о муте в лог
        logger.info(
            f"Пользователю @{member_id} запрещено писать сообщения до {until_date} админом @{admin_id}"
        )

        service_message = await message.reply("Сообщение самоуничтожится через 5 секунд", reply=False)
        await asyncio.sleep(5)
        await message.reply_to_message.delete()

    # Если бот не может замутить пользователя (администратора), возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest:

        # Отправляем сообщение
        await message.reply(
            f"Пользователь {member_mentioned} "
            "является администратором чата, я не могу выдать ему RO",
            reply=False
        )

        service_message = await message.answer(f"Сообщение самоуничтожится через 5 секунд.", reply=False)

        # Вносим информацию о муте в лог
        logger.info(f"Бот не смог замутить пользователя @{member_id}")

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
    try:
        member_id = message.reply_to_message.from_user.id
        member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)
        chat_id = message.chat.id
        admin_id = message.from_user.id
        admin_mentioned = message.from_user.get_mention(as_html=True)

    # Ловим ошибку, если пользователь не переслал сообщение
    except AttributeError:
        await message.reply("Ошибка. Нужно переслать сообщение")
        return False

    # Возвращаем пользователю возможность отправлять сообщения
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=member_id,
        can_send_messages=True
    )

    # Информируем об этом
    await message.answer(f"Пользователь {member_mentioned} был размучен администратором {admin_mentioned}", reply=False)
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.", reply=False)

    # Не забываем про лог
    logger.info(
        f"Пользователь @{member_id} был размучен администратором @{admin_id}"
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
    try:
        member_id = message.reply_to_message.from_user.id
        member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)
        admin_id = message.from_user.id
        admin_mentioned = message.from_user.get_mention(as_html=True)
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
            f"Пользователь @{member_id} был забанен админом @{admin_id}"
        )
        service_message = await message.answer("Сообщение самоуничтожится через 5 секунд.", reply=False)

        # После чего засыпаем на 5 секунд
        await asyncio.sleep(5)

        # Не забываем удалить сообщение, на которое ссылался администратор
        await message.reply_to_message.delete()

    # Если бот не может забанить пользователя (администратора), возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest:

        # Отправляем сообщение
        await message.reply(
            f"Пользователь {member_mentioned} "
            "является администратором чата, я не могу выдать ему RO",
            reply=False
        )

        service_message = await message.answer(f"Сообщение самоуничтожится через 5 секунд.", reply=False)

        # Вносим информацию о бане в лог
        logger.info(f"Бот не смог забанить пользователя @{member_id}")

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
    try:
        member_id = message.reply_to_message.from_user.id
        member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)
        admin_id = message.from_user.id
        admin_mentioned = message.from_user.get_mention(as_html=True)
    # Ловим ошибку, если пользователь не переслал сообщение
    except AttributeError:
        await message.reply("Ошибка. Нужно переслать сообщение")
        return False

    # И разбаниваем
    await message.chat.unban(user_id=member_id)

    # Пишем в чат
    await message.answer(f"Пользователь {member_mentioned} был разбанен", reply=False)
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.", reply=False)

    # Пауза 5 сек
    await asyncio.sleep(5)

    # Записываем в логи
    logger.info(
        f"Пользователь @{member_id} был забанен админом @{admin_id}"
    )

    # Удаляем сообщения
    await message.delete()
    await service_message.delete()
