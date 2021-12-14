from aiogram import executor, types
from loguru import logger

import filters
import middlewares

from data.config import SKIP_UPDATES
from loader import db, dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

middlewares.setup(dp)
filters.setup(dp)

# noinspection PyUnresolvedReferences
import handlers


async def on_startup(dp):
    await set_default_commands(dp)
    await on_startup_notify(dp)
    try:
        db.create_table_stickers()
        db.create_table_chat_admins()
    except Exception as err:
        print(err)

    logger.info("Бот запущен")


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup,
        skip_updates=SKIP_UPDATES,
        allowed_updates=types.AllowedUpdates.all()
    )
