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

metabolism_activity_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Физическая нагрузка отсутсвует или минимальная", callback_data="1.2"),
    ],
    [
        InlineKeyboardButton(text="Тренировки средней тяжести 3 раза в неделю", callback_data="1.38"),
    ],
    [
        InlineKeyboardButton(text="Тренировки средней тяжести 5 раз в неделю", callback_data="1.46"),
    ],
    [
        InlineKeyboardButton(text="Интенсивные тренировки 5 раз в неделю", callback_data="1.55"),
    ],
    [
        InlineKeyboardButton(text="Тренировки каждый день", callback_data="1.64"),
    ],
    [
        InlineKeyboardButton(text="Интенсивные тренировки каждый день или 2 раза в день", callback_data="1.73"),
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])
