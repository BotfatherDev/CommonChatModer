from aiogram import types
from loader import dp


@dp.message_handler()
async def bot_echo(message: types.Message):
    # Получим chat_id и text
    chat_id = message.from_user.id
    text = message.text

    # Получим объект бота - вариант 1 (из диспатчера)
    # bot = dp.bot

    # Получим объект бота - вариант 2 (из контекста)
    # from aiogram import Bot
    # bot = Bot.get_current()

    # Получим объект бота - вариант 3 (из модуля loader)
    from loader import bot

    # Отправим сообщение пользователю - вариант 1
    await bot.send_message(chat_id=chat_id, text=text)

    # Отправим сообщение пользователю - вариант 2 (без ввода chat_id)
    # await message.answer(text=text)

    # Отправим сообщение пользователю - вариант 3 (с реплаем)
    # await message.reply(text=text)

