from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold

from data.config import ADMINS_ID
from filters import IsGroup, IsReplyFilter
from loader import dp, bot


@dp.message_handler(
    IsGroup(),
    IsReplyFilter(True),
    Command("report", prefixes={"/", "!"})
)
async def report_user(message: types.Message):
    if message.from_user.username:
        display_name = f"@{message.from_user.username}"
    else:
        display_name = hbold(message.from_user.first_name)

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
