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
    await help(message)


@dp.message_handler(IsGroup(), Command("help", prefixes="/"))
async def help(message: types.Message):
    """Хендлер на команду /help
    Выводит список комманд."""

    # Отправляем список комманд
    await message.answer(
        "{header1}"                                         "\n"
        "/start - Начать диалог со мной"                    "\n"
        "/help - Помощь по комманде"                        "\n"
                                                            "\n"
        "{header2}"                                         "\n"
        "/ro - Выставить RO пользователю"                   "\n"
        "/unro - Убрать RO у пользователя"                  "\n"
        "/ban - Забанить пользователя"                      "\n"
        "/unban - Разбанить пользователя"                   "\n"
                                                            "\n"
        "{header3}"                                         "\n"
        "/set_photo - Изменить фотку"                       "\n"
        "/set_title - Изменить название"                    "\n"
        "/set_description - Изменить описание"              "\n"
                                                            "\n"
        "{header4}"                                         "\n"
        "/gay [цель*] -  Тест на гея"                       "\n"
        "/biba - Проверить бибу"                            "\n"
        "/roll - Случайное число"                           "\n"
        "/metabolism - Узнать свою суточную норму калорий"  "\n"
                                                            "\n"
        "{warning}".format(
            header1=hbold("Основные комманды"),
            header2=hbold("Администрирование"),
            header3=hbold("Работа с группой"),
            header4=hbold("Другие комманды"),
            warning=hbold("В группах функционал бота может отличаться.\n"
                          "* - необязательный аргумент")
        )
    )
