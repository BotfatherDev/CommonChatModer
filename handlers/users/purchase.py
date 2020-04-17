import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_datas import buy_callback
from keyboards.inline.choice_buttons import choice, pear_keyboard, apples_keyboard
from loader import dp


@dp.message_handler(Command("items"))
async def show_items(message: Message):
    await message.answer(text="На продажу у нас есть 2 товара: 5 Яблок и 1 Груша. \n"
                              "Если вам ничего не нужно - жмите отмену",
                         reply_markup=choice)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "pear"
@dp.callback_query_handler(text_contains="pear")
async def buying_pear(call: CallbackQuery):
    # Обязательно сделать answer, чтобы убрать "часики" после нажатия на кнопку
    await call.answer()

    callback_data = call.data

    # Отобразим что у нас лежит в callback_data
    # logging.info(f"callback_data='{callback_data}'")
    # В питоне 3.8 можно так
    logging.info(f"{callback_data=},  {call.inline_message_id=}, {call.chat_instance=}")

    await call.message.answer("Вы выбрали купить грушу. Груша всего одна. Спасибо.",
                              reply_markup=pear_keyboard)


# Попробуем использовать фильтр от CallbackData
@dp.callback_query_handler(buy_callback.filter(item_name="apple"))
async def buying_apples(call: CallbackQuery, callback_data: dict):
    # Обязательно сделать answer, чтобы убрать "часики" после нажатия на кнопку
    await call.answer(text="kek", cache_time=100)
    logging.info(f"{callback_data=}")

    quantity = callback_data.get("quantity")
    await call.message.answer(f"Вы выбрали купить яблоки. Яблок всего {quantity}. Спасибо.",
                              reply_markup=apples_keyboard)


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы отменили эту покупку!", show_alert=True)

    # Отправляем пустую клваиатуру, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup=None)
