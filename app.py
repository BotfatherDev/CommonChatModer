from aiogram import executor
from loguru import logger

from data.config import SKIP_UPDATES

from loader import db, dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import filters

filters.setup(dp)
import handlers
import middlewares
middlewares.setup(dp)


async def on_startup(dp):
    await set_default_commands(dp)
    await on_startup_notify(dp)
    try:
        db.create_table_stickers()
    except Exception as err:
        print(err)
    logger.info("Бот запущен")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=SKIP_UPDATES)
