import io

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import AdminFilter, Command
from loguru import logger

from filters import IsGroup


async def set_new_photo(message: types.Message):
    source_message = message.reply_to_message
    photo = source_message.photo[-1]
    photo = await photo.download(destination=io.BytesIO())
    input_file = types.InputFile(photo)

    try:
        await message.chat.set_photo(photo=input_file)
        await message.reply("Фотка была успешна обновлена.")
    except Exception as err:
        logger.exception(err)


async def set_new_title(message: types.Message):
    source_message = message.reply_to_message
    title = source_message.text
    # Вариант 1
    # await bot.set_chat_title(message.chat.id, title=title)

    # Вариант 2
    await message.chat.set_title(title=title)


async def set_new_description(message: types.Message):
    source_message = message.reply_to_message
    description = source_message.text

    # Вариант 1
    # await bot.set_chat_description(message.chat.id, description=description)

    # Вариант 2
    await message.chat.set_description(description=description)


def register_edit_chat_handlers(dp: Dispatcher):
    dp.register_message_handler(set_new_photo, IsGroup(), Command("set_photo", prefixes="!/"), AdminFilter())
    dp.register_message_handler(set_new_title, IsGroup(), Command("set_title", prefixes="!/"), AdminFilter())
    dp.register_message_handler(set_new_description, IsGroup(), Command("set_description", prefixes="!/"), AdminFilter())
