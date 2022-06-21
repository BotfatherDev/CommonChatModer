"""Данный файл является аналогом basic.py в /private
Сделанно это для того, чтоб не мешать все в одном хендлере.
Все хендлеры созданы для групп и все изменения
будут видны лишь там."""

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold

from filters import IsGroup


async def start(message: types.Message):
    await message.delete()

    # Выводим список комманд
    # await help_cmd(message)


async def help_cmd(message: types.Message):
    """Хендлер на команду /help
    Выводит список комманд."""

    # Создаем текст
    text = """{header1}
/start - Начать диалог со мной
/help - Помощь по комманде

{header2}
/ro - Выставить RO пользователю
/unro - Убрать RO у пользователя      
/ban - Забанить пользователя
/unban - Разбанить пользователя

{header3}
/set_photo - Изменить фотку
/set_title - Изменить название
/set_description - Изменить описание

{header4}
/gay [цель*] -  Тест на гея
/biba - Проверить бибу
/roll - Случайное число
/metabolism - Узнать свою суточную норму калорий

{warning}
""".format(
        header1=hbold("Основные комманды"),
        header2=hbold("Администрирование"),
        header3=hbold("Работа с группой"),
        header4=hbold("Другие комманды"),
        warning=hbold(
            "В группах функционал бота может отличаться.\n"
            "* - необязательный аргумент"
        )
    )

    # Отправляем список комманд
    await message.answer(text)


def register_basic_handlers(dp: Dispatcher):
    dp.register_message_handler(start, IsGroup(), Command("start"))
    dp.register_message_handler(help_cmd, IsGroup(), Command("help", prefixes="!/"))
