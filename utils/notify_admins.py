from loguru import logger

from aiogram import Dispatcher
from aiogram.utils.exceptions import ChatNotFound

from data.config import ADMINS_ID


async def mail_to_admins(dp):
    for admin in ADMINS_ID:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе с группами!")
        except ChatNotFound:
            logger.error("Чат с админом не найден")
        except Exception as err:
            logger.exception(err)


async def on_startup_notify(dp: Dispatcher):
    await mail_to_admins(dp)
