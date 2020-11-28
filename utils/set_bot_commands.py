from aiogram import types
from loguru import logger


async def set_default_commands(dp):
    logger.info("Установка стандартных комманд-подсказок...")
    await dp.bot.set_my_commands([
        types.BotCommand("set_photo", "(admins only) Установить фото в чате"),
        types.BotCommand("set_title", "(admins only) Установить название группы"),
        types.BotCommand("set_description", "(admins only) Установить описание группы"),
        types.BotCommand("gay", "Узнать, на сколько % пользователь гей"),
        types.BotCommand("metabolism", "Узнать свою суточную норму калорий"),
        # types.BotCommand("roll", "Получить случайное число"),
        types.BotCommand("biba", "Узнать сколько см у пользователя биба"),
        # types.BotCommand("ro", "(admins only) Замутить пользователя"),
        types.BotCommand("unro", "(admins only) Размутить пользователя"),
        # types.BotCommand("ban", "(admins only) Забанить пользователя"),
        types.BotCommand("unban", "(admins only) Разбанить пользователя"),
        types.BotCommand("media_false", "(admins only) Запрещает использование media"),
        types.BotCommand("media_true", "(admins only) Разрешает использование media"),
    ])
