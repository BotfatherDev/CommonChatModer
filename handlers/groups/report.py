import time
import asyncio
from aiogram import types, exceptions
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink

from filters import IsGroup, IsReplyFilter
from loguru import logger
from loader import dp, db

report_command = Command("report", prefixes={"/", "!"})


@dp.message_handler(IsGroup(), IsReplyFilter(True), report_command)
async def report_user(message: types.Message):
    """Отправляет жалобу на пользователя админам"""

    reply = message.reply_to_message

    # Если юзер репортит на сообщение из канала, то пропускаем это
    if reply.is_automatic_forward is True:
        await message.delete()
        return

    # Проверка на то что реплай сообщение написано от имени канала
    if reply.sender_chat:
        mention = reply.sender_chat.title
    else:
        mention = reply.from_user.get_mention()

    chat_id = message.chat.id

    await message.answer(
        f"Репорт на пользователя {mention} успешно отправлен.\n"
        "Администрация предпримет все необходимые меры"
    )

    chat_admins = db.select_all_chat_admins(chat_id)

    if not chat_admins:
        # На всякий случай что бы не было спама
        data = await dp.storage.get_data(chat=chat_id)
        if data.get('last_get_admins_time', 0) < time.time():
            await dp.storage.update_data(
                chat=chat_id,
                data={'last_get_admins_time': time.time() + 3600}
            )

            admins = await dp.bot.get_chat_administrators(chat_id)
            for admin in admins:
                if admin.user.is_bot is False:
                    db.add_chat_admin(chat_id, admin.user.id)

            chat_admins = db.select_all_chat_admins(chat_id)
    logger.info(f"Администраторы группы {chat_id}: {chat_admins}")
    chat_admins = {admin[0] for admin in chat_admins}

    for admin in chat_admins:
        admin_id = admin
        try:
            await dp.bot.send_message(
                chat_id=admin_id,
                text=f"Кинут репорт на пользователя {mention} "
                     "за следующее " + hlink("сообщение", message.reply_to_message.url)
            )
            await asyncio.sleep(0.05)
        except (exceptions.BotBlocked, exceptions.UserDeactivated, exceptions.CantTalkWithBots,
                exceptions.CantInitiateConversation):
            db.del_chat_admin(chat_id, admin_id)
        except Exception as err:
            logger.exception("Не предвиденное исключение при рассылке сообщений админам чата при отправке репорта.")
            logger.exception(err)


@dp.message_handler(IsGroup(), report_command)
async def report_user_if_command_is_not_reply(message: types.Message):
    """Уведомляет, что репорт должен быть ответом"""
    await message.reply(
        "Сообщение с командой должно быть ответом на сообщение пользователя, "
        "на которого вы хотите пожаловаться"
    )
