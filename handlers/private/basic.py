"""Данный файл является аналогом basic.py в /groups
Сделанно это для того, чтоб не мешать все в одном хендлере.
Все хендлеры созданы для личных сообщнений и все изменения
будут видны лишь там"""

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold

from filters import IsPrivate
from keyboards.inline import start_markup
from loader import dp


@dp.message_handler(IsPrivate(), Command("start", prefixes="/"))
async def start(message: types.Message):
    """Хендлер на команду /start
    Приветствует пользователя.
    Используется в личных сообщениях"""

    # Отправляем приветствие
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}\n\n"
                         "Я простой чат-менеджер с открытым исходным кодом, "
                         "который пишется участниками чата по разработке ботов. "
                         "Для полного функционала добавь меня в группу ", reply_markup=start_markup)


@dp.message_handler(IsPrivate(), Command("help", prefixes="/"))
async def help(message: types.Message):
    """Хендлер на команду /help
    Выводит список комманд.
    Используется в личных сообщениях"""

    # Отправляем список комманд
    await message.answer(
        "{header1}"                              "\n"
        "/start - Начать диалог со мной"         "\n"
        "/help - Помощь по комманде"             "\n"
                                                 "\n"
        "{header2}"                              "\n"
        "/gay [цель*] -  Тест на гея"            "\n"
        "/biba - Проверить бибу"                 "\n"
                                                 "\n"
        "{warning}".format(
            header1=hbold("Основные комманды"),
            header2=hbold("Другие комманды"),
            warning=hbold("В группах функционал бота может отличаться.\n"
                          "* - необязательный аргумент")
        )
    )


@dp.callback_query_handler(text='help')
async def callback_handler(query: types.CallbackQuery):
    """Обычный CallBack хендлер,
    который проверяет на что нажал пользователь"""

    # Присваиваем query дату переменной
    answer_data = query.data

    # Отвечаем пользователю, чтоб возле инлайн кнопки
    # не было "часиков", это нужно делать даже когда нечего сказать
    # P.S. пользователь сообщение не увидит без аргумента show_alert=True
    await query.answer()

    # Выводим список комманд, если пользователь нажал на кнопку
    # со списком комманд, которая имеет CB дату "help"
    if answer_data == "help":
        await help(query.message)
