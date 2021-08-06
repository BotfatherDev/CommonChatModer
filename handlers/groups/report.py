from aiogram import types
from aiogram.dispatcher.filters import Command

from data.config import ADMINS_ID
from filters import IsGroup, IsReplyFilter
from loader import dp, bot
from utils.misc.display_name import get_display_name

report_command = Command("report", prefixes={"/", "!"})


@dp.message_handler(IsGroup(), IsReplyFilter(True), report_command)
async def report_user(message: types.Message):
    display_name = get_display_name(message.from_user)

    await message.answer(
        f"Репорт на пользователя {display_name} успешно отправлен.\n"
        "Администрация предпримет все необходимые меры"
    )

    for admin_id in ADMINS_ID:
        await bot.send_message(
            admin_id,
            f"Кинут репорт на пользователя {display_name} "
            f"за следующее сообщение"
        )
        await bot.forward_message(
            admin_id,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id
        )
