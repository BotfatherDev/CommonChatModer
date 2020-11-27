"""TODO
1. В функцию cancel добавить emoji
2. После каждого вопроса предлагать пользователю досрочно завершить процесс
3. Перевести проверку корректности введенных текстовых значений в middleware
4. Вывести пользователю информацию о выбранном поле
5. Вывести пользователю информацию о выбранном уровне активности
6. Протестировать дробные числа при указании роста, веса, возраста
"""


import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ContentType

from keyboards.inline.metabolism import metabolism_gender_markup, metabolism_activity_markup
from loader import dp

from states.metabolism import Metabolism
from utils.misc import metabolism_calculation


@dp.message_handler(Command("metabolism"), state=None)
async def enter_test(message: types.Message):
    await message.answer("Вы начали расчет своего уровня обмена веществ.\n"
                         "Ваш пол?",
                         reply_markup=metabolism_gender_markup)

    await Metabolism.gender.set()


@dp.message_handler(state=Metabolism.gender)
@dp.callback_query_handler(text_contains="male" or "female")
async def answer_gender(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(text=call.data, cache_time=60)

    await state.update_data(gender=call.data)

    await call.message.answer(f"{call.data}")
    await call.message.answer(f"Ваш вес, кг?")
    await Metabolism.weight.set()


@dp.message_handler(content_types=ContentType.TEXT, state=Metabolism.weight)
async def answer_weight(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(weight=int(answer))
    else:
        await message.answer("Нужно ввести число !!!")
        return

    await message.answer("Ваш рост, см?")
    await Metabolism.height.set()


@dp.message_handler(content_types=ContentType.TEXT, state=Metabolism.height)
async def answer_height(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(height=int(answer))
    else:
        await message.answer("Нужно ввести число !!!")
        return

    await message.answer("Ваш возраст, полных лет?")
    await Metabolism.age.set()


@dp.message_handler(content_types=ContentType.TEXT, state=Metabolism.age)
async def answer_age(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(age=int(answer))
    else:
        await message.answer("Нужно ввести число !!!")
        return

    await message.answer("Уровень вашей активности?",
                         reply_markup=metabolism_activity_markup)
    await Metabolism.activity.set()


@dp.message_handler(state=Metabolism.activity)
@dp.callback_query_handler()
async def answer_activity(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(text=f"Коэффициент вашей активности {call.data}", cache_time=60)

    await state.update_data(activity=float(call.data))

    # Достаем переменные
    data = await state.get_data()
    gender = data.get("gender")  # пол мужской/женский
    age = data.get("age")  # возраст, полных лет
    height = data.get("height")  # рост, см
    weight = data.get("weight")  # вес, кг
    activity = data.get("activity")  # коэффициент уровня активности

    result = metabolism_calculation(gender=gender, age=age, height=height, weight=weight, activity=activity)
    print(result)

    await call.message.answer(f"Уровень вашего метаболизма - {result} ККал \n\n")

    await state.finish()


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery, state: FSMContext):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы не узнаете много нового о себе ((((", show_alert=True)

    # Отправляем пустую клавиатуру изменяя сообщение
    await call.message.edit_reply_markup(reply_markup=None)

    await state.finish()
