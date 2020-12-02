from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from emoji import emojize

from keyboards.inline.metabolism import metabolism_gender_markup, metabolism_activity_markup, activity_callback, \
    gender_callback
from loader import dp
from states.metabolism import Metabolism
from utils.misc import metabolism_calculation, rate_limit


@rate_limit(60, "metabolism")
@dp.message_handler(Command("metabolism", prefixes="!/"), state=None)
async def enter_test(message: types.Message):
    await message.answer("Вы начали расчет своего уровня обмена веществ.\n"
                         "Ваш пол?",
                         reply_markup=metabolism_gender_markup)

    await Metabolism.gender.set()


@dp.message_handler(state=Metabolism.gender)
@dp.callback_query_handler(gender_callback.filter())
async def answer_gender(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)

    gender = callback_data.get("value")
    await state.update_data(gender=gender)

    description = callback_data.get("description")
    await call.message.answer(f"{description}")

    await call.message.answer(f"Ваш вес, кг?")
    await Metabolism.weight.set()


@dp.message_handler(state=Metabolism.weight)
async def answer_weight(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(weight=int(answer))
    else:
        await message.answer("Нужно ввести целое число !!!")
        return

    await message.answer("Ваш рост, см?")
    await Metabolism.height.set()


@dp.message_handler(state=Metabolism.height)
async def answer_height(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(height=int(answer))
    else:
        await message.answer("Нужно ввести целое число !!!")
        return

    await message.answer("Ваш возраст, полных лет?")
    await Metabolism.age.set()


@dp.message_handler(state=Metabolism.age)
async def answer_age(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(age=int(answer))
    else:
        await message.answer("Нужно ввести целое число !!!")
        return

    await message.answer("Уровень вашей активности?",
                         reply_markup=metabolism_activity_markup)
    await Metabolism.activity.set()


@dp.message_handler(state=Metabolism.activity)
@dp.callback_query_handler(activity_callback.filter())
async def answer_activity(call: CallbackQuery, callback_data: dict, state: FSMContext):
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

    result = metabolism_calculation(gender=gender, age=age, height=height, weight=weight, activity=activity)

    await call.message.answer(f"УРОВЕНЬ ВАШЕГО МЕТАБОЛИЗМА - {result} ККал \n\n")

    await state.finish()


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery, state: FSMContext):
    # Ответим в окошке с уведомлением!
    await call.answer(f"Вы не узнаете много нового о себе {emojize(':thinking_face:')}", show_alert=True)

    # Отправляем пустую клавиатуру изменяя сообщение
    await call.message.edit_reply_markup(reply_markup=None)

    await state.finish()
