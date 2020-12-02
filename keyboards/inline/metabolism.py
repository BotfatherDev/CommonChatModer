from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

"""универсальная кнопка отмены на все случаи жизни

"""
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
cancel_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        cancel_button]
])

"""клавиатура выбора пола респондента

"""
gender_callback = CallbackData("gender", "description", "value")

metabolism_gender_markup = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Мужской", callback_data=gender_callback.new(description="мужчина", value="male")),
        InlineKeyboardButton(text="Женский", callback_data=gender_callback.new(description="женщина", value="female"))
    ],
    [
        cancel_button
    ]
])

"""клавиатура выбора активности респондента

"""
activity_callback = CallbackData("activity", "description", "coefficient")

metabolism_activity_markup = InlineKeyboardMarkup(row_width=1)

activities = list()

activities.append(
    InlineKeyboardButton(text="Физическая нагрузка отсутсвует или минимальная",
                         callback_data=activity_callback.new(
                             description="нагрузка минимальная",
                             coefficient=1.2)
                         )
)

activities.append(
    InlineKeyboardButton(text="Тренировки средней тяжести 3 раза в неделю",
                         callback_data=activity_callback.new(
                             description="3 раза в неделю",
                             coefficient=1.38)
                         )
)

activities.append(
    InlineKeyboardButton(text="Тренировки средней тяжести 5 раз в неделю",
                         callback_data=activity_callback.new(
                             description="5 раз в неделю",
                             coefficient=1.46)
                         )
)

activities.append(
    InlineKeyboardButton(text="Интенсивные 5 раз в неделю",
                         callback_data=activity_callback.new(
                             description="Интенсивно 5 раз в неделю",
                             coefficient=1.55)
                         )
)

activities.append(
    InlineKeyboardButton(text="Тренировки каждый день",
                         callback_data=activity_callback.new(
                             description="каждый день",
                             coefficient=1.64)
                         )
)

activities.append(
    InlineKeyboardButton(text="Интенсивные тренировки каждый день или 2 раза в день",
                         callback_data=activity_callback.new(
                             description="интенсивно каждый день",
                             coefficient=1.73)
                         )
)

activities.append(cancel_button)

for activity in activities:
    metabolism_activity_markup.insert(activity)
