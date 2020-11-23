from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

metabolism_gender_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Мужской", callback_data="male"),
        InlineKeyboardButton(text="Женский", callback_data="female")
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])
