import sqlite3

from loguru import logger


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_stickers(self):
        sql = """
        CREATE TABLE BannedStickers(
            set_name varchar(255) NOT NULL
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def block_sticker(self, set_name: str):

        sql = """
        INSERT INTO BannedStickers(set_name) VALUES(?)
        """
        self.execute(sql, parameters=(set_name,), commit=True)

    def select_all_sets(self):
        sql = """
        SELECT * FROM BannedStickers
        """
        return self.execute(sql, fetchall=True)

    def create_table_karma_users(self):

        """
        Создаем таблицу с название USERS_KARMA
        колонки:
        user_id : integer
        karma: integer

        """
        sql = """CREATE TABLE USERS_KARMA (
            
            user_id INTEGER PRIMARY KEY,
            karma INTEGER,
            full_name varchar 255
        )
        """
        self.execute(sql, commit=True)

    def update_karma(self, user_id: int, karma: int = 0):

        # если статус update_karma = True, мы обновляем карму
        now_karma = self.select_karma_user(user_id=user_id)[0][1]

        now_karma += karma
        sql = "UPDATE USERS_KARMA SET karma = ? WHERE user_id = ?"
        return self.execute(sql, parameters=(now_karma, user_id), commit=True)

    def add_user(self, user_id: int, full_name: str, karma: int = 0):
        try:
            sql = "INSERT INTO USERS_KARMA (user_id, full_name, karma) VALUES (?,?,?)"
            self.execute(sql, parameters=(user_id, full_name, karma), commit=True)
        except Exception as e:
            logger.info(e)

    def select_karma_user(self, user_id: int):
        """
        Выводим пользователя из базы данных по юзеру
        """
        sql = "SELECT * FROM USERS_KARMA WHERE user_id = ?"
        return self.execute(sql, parameters=(user_id,), fetchall=True)

    def select_karma_top(self, limit: int = 10):
        """
        Функция в котором мы определяем количество топ пользователей
        группы по набранным баллам

        parameters:
        limit - int , default = 10 users
        """

        sql = "SELECT * FROM USERS_KARMA ORDER BY karma DESC"
        setting_limit = " LIMIT " + str(limit)
        sql += setting_limit

        return self.execute(sql, fetchall=True)

# def logger(statement):
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)
