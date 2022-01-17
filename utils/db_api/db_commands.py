from utils.db_api.models import Student


async def get_user(telegram_id):
    return await Student.query.where(Student.telegram_id == telegram_id).gino.first()
