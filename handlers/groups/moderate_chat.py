import asyncio
import datetime
import re

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.exceptions import BadRequest
from loguru import logger

from data.permissions import (set_new_user_approved_permissions,
                              set_no_media_permissions,
                              set_user_ro_permissions)
from filters import IsGroup
from loader import bot, db, dp

restriction_time_regex = re.compile(r'(\b[1-9][0-9]*)([mhds]\b)')


def get_restriction_period(text: str) -> int:
    """
    Extract restriction period (in seconds) from text using regex search
    :param text: text to parse
    :return: restriction period in seconds (0 if nothing found, which means permanent restriction)
    """
    if match := re.search(restriction_time_regex, text):
        time, modifier = match.groups()
        multipliers = {"m": 60, "h": 3600, "d": 86400, "s": 1}
        return int(time) * multipliers[modifier]
    return 0


@dp.message_handler(
    IsGroup(),
    regexp=r"(!ro|/ro) ?(\b[1-9][0-9]\w)? ?([\w+\D]+)?",
    is_reply=True,
    user_can_restrict_members=True,
)
async def read_only_mode(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !ro ИЛИ /ro
    :time int: время на которое нужно замутить пользователя в минутах
    :reason str: причина мута. При отсутствии времени и/или причины, то
    используются стандартные значения: 5 минут и None для времени и причины соответственно"""

    # Создаем переменные для удобства
    (
        admin_username,
        admin_mentioned,
        chat_id,
        member_id,
        member_username,
        member_mentioned,
    ) = get_members_info(message)

    # Разбиваем команду на аргументы с помощью RegExp
    command_parse = re.compile(r"(!ro|/ro) ?(\b[1-9][0-9]\w)? ?([\w+\D]+)?")
    parsed = command_parse.match(message.text)
    reason = parsed.group(3)
    # Проверяем на наличие и корректность срока RO
    # Проверяем на наличие причины
    reason = "без указания причины" if not reason else f"по причине: {reason}"
    # Получаем конечную дату, до которой нужно замутить
    ro_period = get_restriction_period(message.text)
    ro_end_date = message.date + datetime.timedelta(seconds=ro_period)

    try:
        # Пытаемся забрать права у пользователя
        await message.chat.restrict(
            user_id=member_id,
            permissions=set_user_ro_permissions(),
            until_date=ro_end_date,
        )

        # Отправляем сообщение
        await message.answer(
            f"Пользователю {member_mentioned} "
            f"было запрещено писать до {ro_end_date.strftime('%d.%m.%Y %H:%M')} "
            f"администратором {admin_mentioned} {reason} "
        )

        # Вносим информацию о муте в лог
        logger.info(
            f"Пользователю @{member_username} запрещено писать сообщения до "
            f"{ro_end_date.strftime('%d.%m.%Y %H:%M')} админом @{admin_username} "
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
    service_message = await message.reply(
        'Сообщение самоуничтожится через 5 секунд.'
    )

    await asyncio.sleep(5)
    # после прошедших 5 секунд, бот удаляет сообщение от администратора и от самого бота
    await message.delete()
    await service_message.delete()
    await message.reply_to_message.delete()


@dp.message_handler(
    IsGroup(),
    Command(commands=["unro"], prefixes="!/"),
    is_reply=True,
    user_can_restrict_members=True,
)
async def undo_read_only_mode(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !unro ИЛИ /unro"""
    (
        admin_username,
        admin_mentioned,
        chat_id,
        member_id,
        member_username,
        member_mentioned,
    ) = get_members_info(message)

    # Возвращаем пользователю возможность отправлять сообщения
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=member_id,
        permissions=set_new_user_approved_permissions(),
    )

    # Информируем об этом
    await message.answer(
        f"Пользователь {member_mentioned} был размучен администратором {admin_mentioned}"
    )
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


@dp.message_handler(
    IsGroup(),
    Command(commands=["ban"], prefixes="!/"),
    is_reply=True,
    user_can_restrict_members=True,
)
async def ban_user(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !ban ИЛИ /ban"""

    # Создаем переменные для удобства
    admin_fullname = message.from_user.full_name
    admin_mentioned = message.from_user.get_mention(as_html=True)

    message_reply = message.reply_to_message

    if 'sender_chat' not in message_reply:
        member_id = message_reply.from_user.id
        member_fullname = message_reply.from_user.full_name
        member_mentioned = message_reply.from_user.get_mention(as_html=True)

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
    else:
        sender_chat_title = message_reply.sender_chat.title
        sender_chat_id = message_reply.sender_chat.id

        await message.chat.ban_sender_chat(sender_chat_id)
        await message.answer(
            f"Канал '{sender_chat_title}' был успешно забанен администратором {admin_mentioned}"
        )
        logger.info(
            f"Канал '{sender_chat_title}' был забанен админом {admin_fullname}"
        )

    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")

    # После чего засыпаем на 5 секунд
    await asyncio.sleep(5)
    # Не забываем удалить сообщение, на которое ссылался администратор
    await message.reply_to_message.delete()
    await message.delete()
    await service_message.delete()


@dp.message_handler(
    IsGroup(),
    Command(commands=["unban"], prefixes="!/"),
    is_reply=True,
    user_can_restrict_members=True,
)
async def unban_user(message: types.Message):
    """Хендлер с фильтром в группе, где можно использовать команду !unban ИЛИ /unban"""
    # Создаем переменные для удобства
    admin_username = message.from_user.username
    admin_fullname = message.from_user.full_name
    admin_mentioned = message.from_user.get_mention(as_html=True)

    message_reply = message.reply_to_message

    if 'sender_chat' not in message_reply:
        member_id = message_reply.from_user.id
        member_username = message_reply.from_user.username
        member_mentioned = message_reply.from_user.get_mention(as_html=True)

        await message.chat.unban(user_id=member_id)
        await message.answer(
            f"Пользователь {member_mentioned} был разбанен администратором {admin_mentioned}"
        )
        logger.info(
            f"Пользователь @{member_username} был разбанен админом @{admin_username}"
        )
    else:
        sender_chat_title = message_reply.sender_chat.title
        sender_chat_id = message_reply.sender_chat.id

        await message.chat.unban_sender_chat(sender_chat_id)
        await message.answer(
            f"Канал '{sender_chat_title}' был успешно разбанен администратором {admin_mentioned}"
        )
        logger.info(
            f"Канал '{sender_chat_title}' был разбанен админом {admin_fullname}"
        )

    service_message = await message.reply("Сообщение самоуничтожится через 5 секунд.")
    # Пауза 5 сек
    await asyncio.sleep(5)
    # Удаляем сообщения
    await message.delete()
    await service_message.delete()


@dp.message_handler(
    IsGroup(),
    Command(commands=["media_false"], prefixes="!/"),
    is_reply=True,
    user_can_restrict_members=True,
)
async def media_false_handler(message: types.Message):
    (
        admin_username,
        admin_mentioned,
        chat_id,
        member_id,
        member_username,
        member_mentioned,
    ) = get_members_info(message)

    command_parse = re.compile(r"(!media_false|/media_false) ?(\d+)?")
    parsed = command_parse.match(message.text)
    time = parsed.group(2)

    answer_text = f"Пользователь {member_mentioned} было был лишён права использовать медиаконтент "
    if time:
        answer_text += f"на {time} минут\n"
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
            user_id=member_id, permissions=new_permissions, until_date=until_date
        )
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


@dp.message_handler(
    IsGroup(),
    Command(commands=["media_true"], prefixes="!/"),
    is_reply=True,
    user_can_restrict_members=True,
)
async def media_true_handler(message: types.Message):
    (
        admin_username,
        admin_mentioned,
        chat_id,
        member_id,
        member_username,
        member_mentioned,
    ) = get_members_info(message)

    try:
        # Возвращаем пользователю возможность отправлять медиаконтент
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=member_id,
            permissions=set_new_user_approved_permissions(),
        )

        # Информируем об этом
        await message.answer(
            f"Пользователь {member_mentioned} "
            f"благодаря {admin_mentioned} может снова использовать медиаконтент"
        )
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
        message.reply_to_message.from_user.get_mention(as_html=True),
    ]
