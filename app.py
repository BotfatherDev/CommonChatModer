from loguru import logger

from loader import dp, bot, storage
from data.config import SKIP_UPDATES

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import filters
    filters.setup(dp)
    logger.info("Подключение handlers...")
    import handlers
    import middlewares
    middlewares.setup(dp)

    await set_default_commands(dp)
    await on_startup_notify(dp)
    logger.info("Бот запущен")


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=SKIP_UPDATES)
