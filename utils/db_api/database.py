from gino import Gino
from data.config import POSTGRES_URI

db = Gino()


#
# Документация
# http://gino.fantix.pro/en/latest/tutorials/tutorial.html

async def create_db():
    # Устанавливаем связь с базой данных
    await db.set_bind(POSTGRES_URI)

    # Создаем таблицы
    # await db.gino.drop_all()
    await db.gino.create_all()
