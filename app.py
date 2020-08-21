from aiogram import executor
from loguru import logger

from data.config import SKIP_UPDATES

from loader import db, dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import filters
import middlewares


async def on_startup(dp):
    import handlers

    filters.setup(dp)
    logger.info("Подключение handlers...")
    middlewares.setup(dp)

    await set_default_commands(dp)
    await on_startup_notify(dp)
    try:
        db.create_table_stickers()
    except Exception as err:
        print(err)
    logger.info("Бот запущен")


executor.start_polling(dp, on_startup=on_startup, skip_updates=SKIP_UPDATES)
