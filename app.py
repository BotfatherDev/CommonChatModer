from aiogram import executor, types
from loguru import logger

import filters
import middlewares
from data.config import SKIP_UPDATES, WEBHOOK_HOST, WEBAPP_PORT, WEBHOOK, WEBHOOK_PATH
from handlers import register_all_handlers
from loader import db, dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    if WEBHOOK:
        await dp.bot.set_webhook(
            url=WEBHOOK_HOST + WEBHOOK_PATH,
            allowed_updates=types.AllowedUpdates.all()
        )
        status = await dp.bot.get_webhook_info()
        logger.info(f"Webhook status: {status}")

    await set_default_commands(dp)
    await on_startup_notify(dp)

    try:
        db.create_table_stickers()
        db.create_table_chat_admins()
        db.create_table_rating_users()
    except Exception as err:
        print(err)

    logger.info("Бот запущен")


if __name__ == "__main__":
    middlewares.setup(dp)
    filters.setup(dp)

    register_all_handlers(dp)
    if WEBHOOK:
        executor.start_webhook(
            dispatcher=dp,
            check_ip=True,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            host='0.0.0.0',
            port=WEBAPP_PORT,
        )
    else:
        executor.start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            skip_updates=SKIP_UPDATES,
            allowed_updates=types.AllowedUpdates.all()
        )
