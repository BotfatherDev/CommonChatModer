from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("set_photo", "Установить фото в чате"),
        types.BotCommand("set_title", "Установить название группы"),
        types.BotCommand("set_description", "Установить описание группы"),
        types.BotCommand("gay", "Узнать, на сколько % пользователь гей"),
        types.BotCommand("roll", "Получить случайное число"),
        types.BotCommand("biba", "Узнать сколько см у пользователя биба"),
        types.BotCommand("ro", "Замутить пользователя"),
        types.BotCommand("unro", "Размутить пользователя"),
        types.BotCommand("ban", "Забанить пользователя"),
        types.BotCommand("unban", "Разбанить пользователя"),
    ])
