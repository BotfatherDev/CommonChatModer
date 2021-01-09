from aiogram import types
from loguru import logger

from loader import db

def url(user_id: int) -> str:
    return f"tg://user?id={user_id}"

def karma(message: types.Message, karma: int = 1):

    user_id = db.select_karma_user(user_id=message.reply_to_message.from_user.id)

    # если нет юзера в базе
    if len(user_id) == 0:
        db.add_user(user_id=message.reply_to_message.from_user.id,
                    full_name=message.reply_to_message.from_user.full_name)  # добавляем пользователя в базу и даем +1 к карме

    db.update_karma(user_id=message.reply_to_message.from_user.id,
                    karma=karma)
    logger.info(f'Мы обновили карму юзеру {message.reply_to_message.from_user.id}')
    return








