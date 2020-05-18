from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold

from filters import IsGroup, IsPrivate
from keyboards.inline import start_markup
from loader import dp


@dp.message_handler(IsPrivate(), Command("start", prefixes="!/"))
async def start(message: types.Message):
    """Хендлер на команду !/start
    Приветствует пользователя.
    Используется в личных сообщениях"""

    # Отправляем приветствие
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}\n\n"
                         "Я простой чат-менеджер с открытым исходным кодом, "
                         "который пишется участниками чата по разработке ботов. "
                         "Для полного функционала добавь меня в группу ", reply_markup=start_markup)


@dp.message_handler(IsPrivate(), Command("help", prefixes="!/"))
async def help_pm(message: types.Message):
    """Хендлер на команду !/help
    Выводит список комманд.
    Используется в личных сообщениях"""

    # Отправляем список комманд
    await message.answer(
        "{header1}"                                         "\n"
        "/start - Начать диалог со мной"                    "\n"
        "/help [комманда] - Помощь по определенной комманде""\n"
                                                            "\n"
        "{header2}"                                         "\n"
        "/gay [*args] -  Тест на гея"                       "\n"
                                                            "\n"
        "{warning}".format(
            header1=hbold("Основные комманды"),
            header2=hbold("Другие комманды"),
            warning=hbold("В группах функционал бота может отличаться")
        )
    )


@dp.message_handler(IsGroup(), Command("start", prefixes="!/"))
async def start(message: types.Message):
    """Хендлер на команду !/start
    Выводит список комманд в группах
    Из-за ненадобности такой информарции
    в группе"""

    # Отправляем список комманд
    await help_groups(message)


@dp.message_handler(IsGroup(), Command("help", prefixes="!/"))
async def help_groups(message: types.Message):
    """Хендлер на команду /help
    Выводит список комманд."""

    # Отправляем список комманд
    await message.answer(
        "{header1}"                                         "\n"
        "/start - Начать диалог со мной"                    "\n"
        "/help [комманда] - Помощь по определенной комманде""\n"
        "\n"
        "{header2}"                                         "\n"
        "/gay [*args] -  Тест на гея"                       "\n"
        "\n"
        "{header3}"                                         "\n"
        "/ro - Выставить RO пользователю"                   "\n"
        "/unro - Убрать RO у пользователя"                  "\n"
        "/ban - Забанить пользователя"                      "\n"
        "/unban - Разбанить пользователя"                   "\n"
        "\n"
        "{header4}"                                         "\n"
        "/set_photo - Изменить фотку"                       "\n"
        "/set_title - Изменить название"                    "\n"
        "/set_description - Изменить описание"              "\n"
        "/pin - Закрепить сообщение"                        "\n"
        "\n"
        "{warning}".format(
            header1=hbold("Основные комманды"),
            header2=hbold("Другие комманды"),
            header3=hbold("Администрирование"),
            header4=hbold("Работа с групой"),
            warning=hbold("В группах функционал бота может отличаться")
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

    if answer_data == 'help':
        await help_pm(query.message)
