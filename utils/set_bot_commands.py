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
        "ro": "Замутить пользователя",
        "unro": "Размутить пользователя",
        "ban": "Забанить пользователя",
        "unban": "Разбанить пользователя",
        "set_photo": "Установить фото в чате",
        "set_title": "Установить название группы",
        "set_description": "Установить описание группы",
        "media_false": "Запрещает использование media",
        "media_true": "Разрешает использование media",
        **commands_members
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
