from aiogram import types

"""Клавиатура, которая используется 
при стартовом сообщении. (!/start)"""

# Создаем клавиатуру
start_markup = types.InlineKeyboardMarkup(row_width=3)

# Кнопки с CallBack Data
text_and_data = (
    ('Список комманд', 'help'),
)

# Добавляем кнопки с Callback Data
row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
start_markup.row(*row_btns)

# Добавляем обычные кнопки
start_markup.add(
    types.InlineKeyboardButton('Мои исходники', url='https://github.com/Latand/CommonChatModer'),
    types.InlineKeyboardButton('Чатик', url='https://t.me/bot_devs_novice'),
)


source_markup = types.InlineKeyboardMarkup()
source_markup.insert(
    types.InlineKeyboardButton('Исходники бота', url='https://github.com/Latand/CommonChatModer'),
)
