from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hlink

from data.config import ADMINS_ID
from filters import IsGroup, IsReplyFilter
from loader import dp, bot
from utils.misc.display_name import get_display_name

report_command = Command("report", prefixes={"/", "!"})


@dp.message_handler(IsGroup(), IsReplyFilter(True), report_command)
async def report_user(message: types.Message):
    """Отправляет жалобу на пользователя админам"""
    display_name = get_display_name(message.reply_to_message.from_user)

    await message.answer(
        f"Репорт на пользователя {display_name} успешно отправлен.\n"
        "Администрация предпримет все необходимые меры"
    )

    for admin_id in ADMINS_ID:
        await bot.send_message(
            admin_id,
            f"Кинут репорт на пользователя {display_name} "
            "за следующее " + hlink("сообщение", message.reply_to_message.url)
        )


@dp.message_handler(IsGroup(), report_command)
async def report_user_if_command_is_not_reply(message: types.Message):
    """Уведомляет, что репорт должен быть ответом"""
    await message.reply(
        "Сообщение с командой должно быть ответом на сообщение пользователя, "
        "на которого вы хотите пожаловаться"
    )
