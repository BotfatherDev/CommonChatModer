from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

metabolism_gender_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Мужской", callback_data="male"),
        InlineKeyboardButton(text="Женский", callback_data="female")
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])

# Формируем клавиатуру видов активностей

activity_callback = CallbackData("activity", "description", "coefficient")

metabolism_activity_markup = InlineKeyboardMarkup(row_width=1)

activities = list()

activities.append(
    InlineKeyboardButton(text="Физическая нагрузка отсутсвует или минимальная",
                         callback_data=activity_callback.new(
                             description="Физическая нагрузка отсутсвует или минимальная",
                             coefficient=1.2)
                         )
)

activities.append(
    InlineKeyboardButton(text="Тренировки средней тяжести 3 раза в неделю",
                         callback_data=activity_callback.new(
                             description="Тренировки средней тяжести 3 раза в неделю",
                             coefficient=1.38)
                         )
)

activities.append(
    InlineKeyboardButton(text="Тренировки средней тяжести 5 раз в неделю",
                         callback_data=activity_callback.new(
                             description="Тренировки средней тяжести 5 раз в неделю",
                             coefficient=1.46)
                         )
)

activities.append(
    InlineKeyboardButton(text="Интенсивные тренировки 5 раз в неделю",
                         callback_data=activity_callback.new(
                             description="Интенсивные тренировки 5 раз в неделю",
                             coefficient=1.55)
                         )
)

activities.append(
    InlineKeyboardButton(text="Тренировки каждый день",
                         callback_data=activity_callback.new(
                             description="Тренировки каждый день",
                             coefficient=1.64)
                         )
)

activities.append(
    InlineKeyboardButton(text="Интенсивные тренировки каждый день или 2 раза в день",
                         callback_data=activity_callback.new(
                             description="Интенсивные тренировки каждый день или 2 раза в день",
                             coefficient=1.73)
                         )
)

activities.append(
    InlineKeyboardButton(text="Отмена", callback_data="cancel")
)

for activity in activities:
    metabolism_activity_markup.insert(activity)

#
# metabolism_activity_markup = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text="Физическая нагрузка отсутсвует или минимальная", callback_data="1.2"),
#     ],
#     [
#         InlineKeyboardButton(text="Тренировки средней тяжести 3 раза в неделю", callback_data="1.38"),
#     ],
#     [
#         InlineKeyboardButton(text="Тренировки средней тяжести 5 раз в неделю", callback_data="1.46"),
#     ],
#     [
#         InlineKeyboardButton(text="Интенсивные тренировки 5 раз в неделю", callback_data="1.55"),
#     ],
#     [
#         InlineKeyboardButton(text="Тренировки каждый день", callback_data="1.64"),
#     ],
#     [
#         InlineKeyboardButton(text="Интенсивные тренировки каждый день или 2 раза в день", callback_data="1.73"),
#     ],
#     [
#         InlineKeyboardButton(text="Отмена", callback_data="cancel")
#     ]
# ])
