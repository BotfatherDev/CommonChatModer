from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from emoji import emojize

from keyboards.inline.metabolism import (activity_callback, gender_callback,
                                         metabolism_activity_markup,
                                         metabolism_gender_markup)
from states.metabolism import Metabolism
from utils.misc import metabolism_calculation, rate_limit


@rate_limit(60, "metabolism")
async def enter_test(message: types.Message):
    await message.answer(
        "Вы начали расчет своего уровня обмена веществ.\n" "Ваш пол?",
        reply_markup=metabolism_gender_markup,
    )

    await Metabolism.gender.set()


async def answer_gender(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)

    gender = callback_data.get("value")
    await state.update_data(gender=gender)

    description = callback_data.get("description")
    await call.message.answer(f"{description}")

    await call.message.answer(f"Ваш вес, кг?")
    await Metabolism.weight.set()


async def answer_weight(message: types.Message, state: FSMContext):
    answer = message.text

    if not answer.isdigit():
        return await message.answer("Нужно ввести целое число !!!")

    await state.update_data(weight=int(answer))

    await message.answer("Ваш рост, см?")
    await Metabolism.height.set()


async def answer_height(message: types.Message, state: FSMContext):
    answer = message.text

    if not answer.isdigit():
        return await message.answer("Нужно ввести целое число !!!")

    await state.update_data(height=int(answer))

    await message.answer("Ваш возраст, полных лет?")
    await Metabolism.age.set()


async def answer_age(message: types.Message, state: FSMContext):
    answer = message.text

    if not answer.isdigit():
        return await message.answer("Нужно ввести целое число !!!")

    await state.update_data(age=int(answer))

    await message.answer(
        "Уровень вашей активности?", reply_markup=metabolism_activity_markup
    )

    await Metabolism.activity.set()


async def answer_activity(call: CallbackQuery, state: FSMContext, callback_data: dict = None):
    if isinstance(call, types.CallbackQuery):
        await call.message.edit_reply_markup(reply_markup=None)

        coefficient = callback_data.get("coefficient")
        await state.update_data(activity=float(coefficient))

        description = callback_data.get("description")
        await call.message.answer(text=f"{description}\n\n")

    # Достаем переменные
    data = await state.get_data()
    gender = data.get("gender")  # пол мужской/женский
    age = data.get("age")  # возраст, полных лет
    height = data.get("height")  # рост, см
    weight = data.get("weight")  # вес, кг
    activity = data.get("activity")  # коэффициент уровня активности

    result = metabolism_calculation(
        gender=gender, age=age, height=height, weight=weight, activity=activity
    )

    await call.message.answer(f"УРОВЕНЬ ВАШЕГО МЕТАБОЛИЗМА - {result} ККал \n\n")

    await state.finish()


async def cancel_metabolism(call: CallbackQuery, state: FSMContext):
    # Ответим в окошке с уведомлением!
    await call.answer(
        f"Вы не узнаете много нового о себе {emojize(':thinking_face:')}",
        show_alert=True,
    )

    # Отправляем пустую клавиатуру изменяя сообщение
    await call.message.edit_reply_markup(reply_markup=None)

    await state.finish()


def register_metabolism_handlers(dp: Dispatcher):
    dp.register_message_handler(enter_test, Command("metabolism", prefixes="!/"), chat_type=types.ChatType.PRIVATE)
    dp.register_callback_query_handler(
        answer_gender, gender_callback.filter(), state=Metabolism.gender
    )
    dp.register_message_handler(answer_weight, state=Metabolism.weight)
    dp.register_message_handler(answer_height, state=Metabolism.height)
    dp.register_message_handler(answer_age, state=Metabolism.age)
    dp.register_callback_query_handler(answer_activity, activity_callback.filter(), state=Metabolism.activity)
    dp.register_callback_query_handler(cancel_metabolism, text="cancel", state='*')
