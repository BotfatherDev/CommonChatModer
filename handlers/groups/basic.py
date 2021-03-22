"""Данный файл является аналогом basic.py в /private
Сделанно это для того, чтоб не мешать все в одном хендлере.
Все хендлеры созданы для групп и все изменения
будут видны лишь там."""

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold

from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), Command("start", prefixes="!/"))
async def start(message: types.Message):
    """Хендлер на команду !/start
    Выводит список комманд из-за ненужности информации
    в группе, которая находиться в приветствии"""

    # Выводим список комманд
    await help_cmd(message)


@dp.message_handler(IsGroup(), Command("help", prefixes="!/"))
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
