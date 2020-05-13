from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold

from loader import dp


@dp.message_handler(Command("start", prefixes="!/"))
async def start(message: types.Message):

    """Хендлер на команду /start
    используется лишь в личных сообщениях.
    В группах выводит список комманд из-за
    того, что та информация особо не нужна в группах"""

    # Проверяем была ли вызвана комманда из личных сообщений
    if types.ChatType.is_private(message):

        # Создаем текст, которым будет отвечать
        text = (
            "Привет, {user}\n\n"
            "Я простой чат-менеджер с открытым кодом, "
            "который пишется участниками чата"
            "по разработке ботов"
        ).format(
            user=hbold(message.from_user.full_name),
            command="/help"
        )

        # Создаем клавиатуру
        keyboard_markup = types.InlineKeyboardMarkup(row_width=3)

        # Кнопки с CallBack Data
        text_and_data = (
            ('Помощь', 'help'),
        )

        # Добавляем кнопки с Callback Data
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)

        # Добавляем обычные кнопки
        keyboard_markup.add(
            types.InlineKeyboardButton('Мои исходники', url='https://github.com/Latand/CommonChatModer'),
            types.InlineKeyboardButton('Чатик', url='https://t.me/bot_devs_novice'),
        )

        # Отправляем сообщение
        await message.reply(text, reply_markup=keyboard_markup)

    # Если комманда была вызвана в группе, то отправляем список комманд
    else:
        await help(message)


@dp.message_handler(Command("help", prefixes="!/"))
async def help(message: types.Message):

    """Хендлер на команду /help
    Выводит список комманд."""

    # Создаем текст, которым будем отвечать
    text = [
        hbold("\n\nОсновные комманды"),
        "\n{command} - Начать диалог со мной".format(command="/start"),
        "\n{command} - Это сообщение".format(command="/help"),
        hbold("\n\nФан-комманды"),
        "\n{command} [args] - Проверить на сколько ты или указанный обьект гей".format(command="/gay"),
    ]

    # Проверяем была ли вызвана комманда в личных сообщениях
    if types.ChatType.is_private(message):
        text.extend(
            [
                hbold("\n\nВ чатах список может отличаться")
            ]
        )
    # Если комманда все же была вызвана с группы, то добавляем комманды доступные лишь в группах
    else:
        text.extend(
            [
                hbold("\n\nАдминистрирование чата"),
                "\n{command} - Выставить RO пользователю".format(command="/ro"),
                "\n{command} - Убрать RO у пользователя".format(command="/unro"),
                "\n{command} - Забанить пользователя".format(command="/ban"),
                "\n{command} - Разбанить пользователя".format(command="/unban"),
                hbold("\n\nРабота с группой"),
                "\n{command} - Изменить фотку".format(command="/set_photo"),
                "\n{command} - Изменить название".format(command="/set_title"),
                "\n{command} - Изменить описание".format(command="/set_description"),
                "\n{command} - Закрепить сообщение".format(command="/pin"),
                hbold("\n\nВ приватных сообщениях список комманд может отличаться."),
            ]
        )

    # Отправляем сообщение
    await message.reply("".join(text))


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
        await help(query.message)