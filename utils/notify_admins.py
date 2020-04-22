import logging

from aiogram import Dispatcher, types

from data.config import admins


async def mail_to_admins(dp):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("set_photo", "Установить фото в чате"),
        types.BotCommand("set_title", "Установить название группы"),
        types.BotCommand("set_description", "Установить описание группы"),
    ])


async def on_startup_notify(dp: Dispatcher):
    await mail_to_admins(dp)
    await set_default_commands(dp)
