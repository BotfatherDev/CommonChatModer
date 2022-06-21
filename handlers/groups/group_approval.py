import random

from aiogram import Dispatcher
from aiogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hlink, hbold

approval_cb = CallbackData('chat_join_request', 'approve', 'chat_id')


async def process_chat_invite_request(chat_join_request: ChatJoinRequest):
    approve_buttons = [
        InlineKeyboardButton(text='🐈',
                             callback_data=approval_cb.new(approve='cat',
                                                           chat_id=chat_join_request.chat.id)),
        InlineKeyboardButton(text='🐶',
                             callback_data=approval_cb.new(approve='dog',
                                                           chat_id=chat_join_request.chat.id)),
        InlineKeyboardButton(text='🐬',
                             callback_data=approval_cb.new(approve='dolphin',
                                                           chat_id=chat_join_request.chat.id)),
    ]
    random.shuffle(approve_buttons)
    text = '\n'.join(
        [
            'Обязательно прочитайте ' + hlink(
                'правила чата ',
                'https://t.me/bot_devs_novice/509927'
            ) + 'для принятия в группу!',
            'Группа создана для обсуждения вопросов связанных и не связанных с разработкой ботов',
            "",
            "Также, ознакомьтесь с бесплатными уроками на сайте https://botfather.dev, "
            "если вы пришли сюда научиться писать ботов."
            "",
            "",
            hbold('После прочтения нажмите на кнопку с котиком'),
        ]
    )
    await chat_join_request.bot.send_message(
        chat_join_request.from_user.id,
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[approve_buttons])
    )


async def approve_callback_group_captcha(call: CallbackQuery, callback_data: dict):
    await call.message.delete_reply_markup()
    await call.message.answer('Вы были приняты в группу!')
    chat_id = callback_data['chat_id']

    await call.bot.approve_chat_join_request(chat_id, call.from_user.id)


async def decline_callback_group_captcha(call: CallbackQuery, callback_data: dict):
    await call.message.delete_reply_markup()
    await call.message.answer('Вы не прошли проверку!')
    chat_id = callback_data['chat_id']

    await call.bot.decline_chat_join_request(chat_id, call.from_user.id)


def register_group_approval(dp: Dispatcher):
    dp.register_chat_join_request_handler(process_chat_invite_request)
    dp.register_callback_query_handler(approve_callback_group_captcha,
                                       approval_cb.filter(approve='cat'))
    dp.register_callback_query_handler(decline_callback_group_captcha,
                                       approval_cb.filter())
