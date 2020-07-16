from loguru import logger

from aiogram import Dispatcher
from aiogram.utils.exceptions import ChatNotFound

from data.config import ADMINS_ID


async def on_startup_notify(dp: Dispatcher):
    logger.info("Оповещение администрации...")
    for admin in ADMINS_ID:
        try:
            await dp.bot.send_message(admin, "Бот был успешно запущен", disable_notification=True)
        except ChatNotFound:
            logger.debug("Чат с админом не найден")
