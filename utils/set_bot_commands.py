from aiogram import Dispatcher, types
from aiogram.types import BotCommand
from loguru import logger


async def set_default_commands(dp: Dispatcher):
    """
    Ставит стандартные команды бота
    """

    logger.info("Установка стандартных команд-подсказок...")

    commands_members = {
        "gay": "Узнать, на сколько % пользователь гей",
        "biba": "Узнать сколько см у пользователя биба",
        "top_helpers": "Узнать топ хелперов"
    }
    command_defaults = {
        'help': 'Help me'
    }
    commands_admins = {
        "set_photo": "(admins only) Установить фото в чате",
        "set_title": "(admins only) Установить название группы",
        "set_description": "(admins only) Установить описание группы",
        "unro": "(admins only) Размутить пользователя",
        "unban": "(admins only) Разбанить пользователя",
        "media_false": "(admins only) Запрещает использование media",
        "media_true": "(admins only) Разрешает использование media",
    }
    await dp.bot.set_my_commands(
        [BotCommand(name, value) for name, value in command_defaults.items()],
        scope=types.BotCommandScopeDefault()
    )
    await dp.bot.set_my_commands(
        [BotCommand(name, value) for name, value in commands_members.items()],
        scope=types.BotCommandScopeAllGroupChats()
    )
    await dp.bot.set_my_commands(
        [BotCommand(name, value) for name, value in commands_admins.items()],
        scope=types.BotCommandScopeAllChatAdministrators()
    )
    logger.info('Команды назначены.')

