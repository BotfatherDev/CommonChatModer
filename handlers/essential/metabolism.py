import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from keyboards.inline.metabolism import metabolism_gender_markup
from loader import dp

# Сделаем фильтр на комманду /metabolism, где не будет указано никакого состояния
from states.metabolism import Metabolism


@dp.message_handler(Command("metabolism"), state=None)
async def enter_test(message: types.Message):
    await message.answer("Вы начали расчет своего уровня обмена веществ.\n"
                         "Вопрос №1. \n\n"
                         "Ваш пол?",
                         reply_markup=metabolism_gender_markup)

    await Metabolism.gender.set()


@dp.message_handler(state=Metabolism.gender)
@dp.callback_query_handler(text_contains="male")
async def answer_gender(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    print(type(call.data), call.data)
    await state.update_data(gender=call.data)

    await state.finish()

    # Вариант 3 - через state.proxy
    # async with state.proxy() as data:
    #     data["answer1"] = answer
    #     # Удобно, если нужно сделать data["some_digit"] += 1
    #     # Или data["some_list"].append(1), т.к. не нужно сначала доставать из стейта, А потом задавать
    #
    # await message.answer("Вопрос №2. \n\n"
    #                      "Ваша память ухудшилась и вы помните то, что было давно, но забываете недавние события?")
    #
    # await Test.next()