from aiogram.types import BotCommand
from loguru import logger


async def set_default_commands(dp):
    """
    Ставит стандартные комманды бота
    """

    logger.info("Установка стандартных комманд-подсказок...")
    
    # TODO: Переместить это в нормальное место
    commands = {
        "set_photo": "(admins only) Установить фото в чате",
        "set_title": "(admins only) Установить название группы",
        "set_description": "(admins only) Установить описание группы",
        # no u
        "gay": "Узнать, на сколько % пользователь гей",
        "metabolism": "Узнать свою суточную норму калорий",
        "biba": "Узнать сколько см у пользователя биба",
        "unro": "(admins only) Размутить пользователя",
        "unban": "(admins only) Разбанить пользователя",
        "media_false": "(admins only) Запрещает использование media",
        "media_true": "(admins only) Разрешает использование media",
    }

    await dp.bot.set_my_commands(
        [BotCommand(name, value) for name, value in commands.items()]
    )

