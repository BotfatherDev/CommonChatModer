from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# создём CallbackData для удобного парсинга калбеков
user_callback = CallbackData("confirm", "being", "user_id")


def generate_confirm_markup(user_id: int) -> InlineKeyboardMarkup:
    """
    Функция, создающая клавиатуру для подтверждения, что пользователь не является ботом
    """

    # создаём инлайн клавиатуру
    confirm_user_markup = InlineKeyboardMarkup(row_width=2)

    # и добавляем в неё 2 кнопки
    confirm_user_markup.add(
        # кнопка "человек", в калбеке которой будет лежать confirm:human:<user_id>
        InlineKeyboardButton(
            "Я человек",
            callback_data=user_callback.new(
                being="human",
                user_id=user_id,
            )
        ),
        # и кнопка "bot", в калбеке которой будет лежать confirm:bot:<user_id>
        InlineKeyboardButton(
            "Я бот",
            callback_data=user_callback.new(
                being="bot",
                user_id=user_id,
            )
        ),
    )

    # отдаём клавиатуру после создания
    return confirm_user_markup
