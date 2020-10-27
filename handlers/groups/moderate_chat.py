import asyncio
import datetime
import re

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest
from loguru import logger

from data.permissions import set_user_ro_permissions, set_new_user_approved_permissions, set_no_media_permissions
from filters import IsGroup
from loader import bot, dp, db


@dp.message_handler(
    IsGroup(),
    regexp=r"(!ro|/ro) ?(\d+)? ?([\w+\D]+)?",
    is_reply=True,
    user_can_restrict_members=True,
)
async def read_only_mode(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !ro ИЛИ /ro
    :time int: время на которое нужно замутить пользователя в минутах
    :reason str: причина мута. При отсуствии времени и/или причины, то
    используються стандартные значения: 5 минут и None для времени и причины соответсвенно"""

    # Создаем переменные для удобства
    admin_username, admin_mentioned, chat_id, member_id, member_username, member_mentioned = get_members_info(message)

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
        reason = f"по причине: {reason}"
    # Получаем конечную дату, до которой нужно замутить
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(time))

    try:
        # Пытаемся забрать права у пользователя
        await message.chat.restrict(
            user_id=member_id,
            permissions=set_user_ro_permissions(),
            until_date=until_date,
        )

        # Отправляем сообщение
        await message.answer(
            f"Пользователю {member_mentioned} "
            f"было запрещено писать на {time} минут "
            f"администратором {admin_mentioned} {reason} ")

        # Вносим информацию о муте в лог
        logger.info(
            f"Пользователю @{member_username} запрещено писать сообщения до {until_date} админом @{admin_username}"
        )

    # Если бот не может замутить пользователя (администратора), возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest:
        # Отправляем сообщение
        await message.answer(
            f"Пользователь {member_mentioned} "
            "является администратором чата, я не могу выдать ему RO"
        )
        # Вносим информацию о муте в лог
        logger.info(f"Бот не смог замутить пользователя @{member_username}")
    service_message = await message.reply(f"Сообщение самоуничтожится через 5 секунд.")
    await asyncio.sleep(5)
    # после прошедших 5 секунд, бот удаляет сообщение от администратора и от самого бота
    await message.delete()
    await service_message.delete()
    await message.reply_to_message.delete()


@dp.message_handler(IsGroup(), Command(commands=["unro"], prefixes="!/"), is_reply=True, user_can_restrict_members=True)
async def undo_read_only_mode(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !unro ИЛИ /unro"""
    admin_username, admin_mentioned, chat_id, member_id, member_username, member_mentioned = get_members_info(message)

    # Возвращаем пользователю возможность отправлять сообщения
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=member_id,
        permissions=set_new_user_approved_permissions(),
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


@dp.message_handler(IsGroup(), Command(commands=["ban"], prefixes="!/"), is_reply=True, user_can_restrict_members=True)
async def ban_user(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !ban ИЛИ /ban"""

    # Создаем переменные для удобства
    admin_fullname = message.from_user.full_name
    admin_mentioned = message.from_user.get_mention(as_html=True)
    member_id = message.reply_to_message.from_user.id
    member_fullname = message.reply_to_message.from_user.full_name
    member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)
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
    except BadRequest:

        # Отправляем сообщение
        await message.answer(
            f"Пользователь {member_mentioned} "
            "является администратором чата, я не могу выдать ему RO"
        )

        logger.info(f"Бот не смог забанить пользователя {member_fullname}")

    service_message = await message.answer("Сообщение самоуничтожится через 5 секунд.")

    # После чего засыпаем на 5 секунд
    await asyncio.sleep(5)
    # Не забываем удалить сообщение, на которое ссылался администратор
    await message.reply_to_message.delete()
    await message.delete()
    await service_message.delete()


@dp.message_handler(IsGroup(), Command(commands=["unban"], prefixes="!/"), is_reply=True,
                    user_can_restrict_members=True)
async def unban_user(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !unban ИЛИ /unban"""

    # Создаем переменные для удобства
    admin_username = message.from_user.username
    admin_mentioned = message.from_user.get_mention(as_html=True)
    member_id = message.reply_to_message.from_user.id
    member_username = message.reply_to_message.from_user.username
    member_mentioned = message.reply_to_message.from_user.get_mention(as_html=True)

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


@dp.message_handler(IsGroup(), Command(commands=["media_false"], prefixes="!/"), is_reply=True,
                    user_can_restrict_members=True)
async def media_false_handler(message: types.Message):
    admin_username, admin_mentioned, chat_id, member_id, member_username, member_mentioned = get_members_info(message)

    command_parse = re.compile(r"(!media_false|/media_false) ?(\d+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)

    answer_text = f"Пользователь {member_mentioned} было был лишён права использовать медиаконтент "
    if time:
        answer_text += f'на {time} минут\n'
    answer_text += f"администратором {admin_mentioned}"

    # Проверяем на наличие и корректность срока media_false
    if not time:
        # мение 30 секунд -- навсегда (время в минутах)
        time = 50000

    # Получаем конечную дату, до которой нужно замутить
    until_date = datetime.datetime.now() + datetime.timedelta(minutes=int(time))

    # Пытаемся забрать права у пользователя
    new_permissions = set_no_media_permissions()
    try:
        logger.info(f"{new_permissions.__dict__}")
        await message.chat.restrict(
            user_id=member_id,
            permissions=new_permissions,
            until_date=until_date)
        # Вносим информацию о муте в лог
        logger.info(
            f"Пользователю @{member_username} запрещено использовать медиаконтент до {until_date} "
            f"админом @{admin_username}"
        )
    # Если бот не может изменить права пользователя (администратора),
    # возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest as err:
        # Отправляем сообщение
        await message.answer(
            f"Пользователь {member_mentioned} "
            "является администратором чата, изменить его права"
        )

        # Вносим информацию о муте в лог
        logger.info(f"Бот не смог забрать права у пользователя @{member_username}")

    # Отправляем сообщение
    await message.answer(text=answer_text)
    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд")
    await asyncio.sleep(5)
    await message.reply_to_message.delete()
    await message.delete()
    await service_message.delete()


@dp.message_handler(IsGroup(), Command(commands=["d"], prefixes="!/"), is_reply=True)
async def block_sticker(message: types.Message):
    member = await message.chat.get_member(message.from_user.id)
    if not member.status == types.ChatMemberStatus.CREATOR:
        return

    try:
        set_name = message.reply_to_message.sticker.set_name
    except Exception:
        return
    db.block_sticker(set_name=set_name)
    await message.reply_to_message.delete()
    await message.reply("Стикерсет Забанен")


@dp.message_handler(IsGroup(), Command(commands=["media_true"], prefixes="!/"), is_reply=True,
                    user_can_restrict_members=True)
async def media_true_handler(message: types.Message):
    admin_username, admin_mentioned, chat_id, member_id, member_username, member_mentioned = get_members_info(message)

    try:
        # Возвращаем пользователю возможность отправлять медиаконтент
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=member_id,
            permissions=set_new_user_approved_permissions(),
        )

        # Информируем об этом
        await message.answer(f"Пользователь {member_mentioned} "
                             f"благодаря {admin_mentioned} может снова использовать медиаконтент")
        logger.info(
            f"Пользователь @{member_username} благодаря @{admin_username} может снова использовать медиаконтент"
        )

        # Если бот не может забрать права пользователя (администратора),
        # возникает ошибка BadRequest которую мы обрабатываем
    except BadRequest:

        # Отправляем сообщение
        await message.answer(
            f"Пользователь {member_mentioned} "
            "является администратором чата, изменить его права"
        )
        # Вносим информацию о муте в лог
        logger.info(f"Бот не смог вернуть права пользователю @{member_username}")

    service_message = await message.reply(f"Сообщение самоуничтожится через 5 секунд.")
    await asyncio.sleep(5)
    await message.delete()
    await service_message.delete()
    await message.reply_to_message.delete()


def get_members_info(message: types.Message):
    # Создаем переменные для удобства
    return [
        message.from_user.username,
        message.from_user.get_mention(as_html=True),
        message.chat.id,
        message.reply_to_message.from_user.id,
        message.reply_to_message.from_user.username,
        message.reply_to_message.from_user.get_mention(as_html=True)
    ]
