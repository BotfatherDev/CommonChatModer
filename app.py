from loader import bot, storage
from data.config import SKIP_UPDATES


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    from utils.set_bot_commands import set_default_commands
    await on_startup_notify(dp)
    await set_default_commands(dp)


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=SKIP_UPDATES)
