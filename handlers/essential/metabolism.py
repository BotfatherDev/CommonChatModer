import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ContentType

from keyboards.inline.metabolism import metabolism_gender_markup, metabolism_activity_markup
from loader import dp

# Сделаем фильтр на комманду /metabolism, где не будет указано никакого состояния
from states.metabolism import Metabolism


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
    await call.message.answer(f"Ваш вес, кг?",
                              reply_markup=None)
    await Metabolism.weight.set()


@dp.message_handler(content_types=ContentType.TEXT, state=Metabolism.weight)
async def answer_gender(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(weight=int(answer))
    else:
        await message.answer("Нужно ввести число !!!"),

    await message.answer("Ваш рост, см?",
                         reply_markup=None)
    await Metabolism.height.set()


@dp.message_handler(content_types=ContentType.TEXT, state=Metabolism.height)
async def answer_gender(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(height=int(answer))
    else:
        await message.answer("Нужно ввести число !!!"),

    await message.answer("Ваш возраст, полных лет?",
                         reply_markup=None)
    await Metabolism.age.set()


@dp.message_handler(content_types=ContentType.TEXT, state=Metabolism.age)
async def answer_gender(message: types.Message, state: FSMContext):
    answer = message.text

    if answer.isdigit():
        await state.update_data(age=int(answer))
    else:
        await message.answer("Нужно ввести число !!!"),

    # Достаем переменные
    data = await state.get_data()
    gender = data.get("gender")  # пол мужской/женский
    age = data.get("age")  # возраст, полных лет
    height = data.get("height")  # рост, см
    weight = data.get("weight")  # вес, кг

    await message.answer("Уровень вашей активности?",
                         reply_markup=metabolism_activity_markup)
    await Metabolism.activity.set()


@dp.message_handler(state=Metabolism.activity)
@dp.callback_query_handler()
async def answer_gender(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer(text=f"Коэффициент вашей активности {call.data}", cache_time=60)

    await state.update_data(activity=int(call.data))

    # await message.answer(f"Ваши данные: "
    #                      f"пол {gender}, "
    #                      f"возраст {age} лет, "
    #                      f"{height} см рост, "
    #                      f"{weight} кг вес"
    #                      )

    await state.finish()


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery, state: FSMContext):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы не узнаете много нового о себе ((((", show_alert=True)

    # Отправляем пустую клавиатуру изменяя сообщение
    await call.message.edit_reply_markup(reply_markup=None)

    await state.finish()
