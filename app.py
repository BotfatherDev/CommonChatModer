from aiogram import executor, types
from loguru import logger

import filters
import middlewares

from data.config import SKIP_UPDATES
from loader import db, dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


from aiohttp import web

from data import config
from data.config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, ip
from loader import SSL_CERTIFICATE, ssl_context, bot
from utils.set_bot_commands import set_default_commands
from webserver.handler import app, dp

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
        db.create_table_rating_users()
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



async def on_startup(app):
    await bot.set_webhook(
        url=WEBHOOK_URL,
        certificate=SSL_CERTIFICATE
    )

    webhook = await bot.get_webhook_info()
    import filters
    import middlewares

    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


app.on_startup.append(on_startup)
web.run_app(app, host="0.0.0.0", port=config.WEBHOOK_PORT, ssl_context=ssl_context)