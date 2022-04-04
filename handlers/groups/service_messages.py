import asyncio
import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.permissions import (set_new_user_approved_permissions,
                              set_new_user_permissions)
from filters import IsGroup
from keyboards.inline import (generate_confirm_markup, source_markup,
                              user_callback)
from loader import bot, dp, db


@dp.message_handler(content_types="new_chat_members")
async def on_user_join(message: types.Message, state: FSMContext):
    await state.update_data(service_message=message)


@dp.chat_member_handler()
async def updated_chat_member(chat_member_updated: types.ChatMemberUpdated):
    """Хендлер для вышедших либо кикнутых пользователей"""

    performer_mention = chat_member_updated.from_user.get_mention(as_html=True)
    member_mention = chat_member_updated.old_chat_member.user.get_mention(as_html=True)

    bot_user = await dp.bot.me
    if chat_member_updated.from_user.id == bot_user.id:
        return False

    if chat_member_updated.new_chat_member.status == types.ChatMemberStatus.MEMBER:
        state = dp.current_state(chat=chat_member_updated.chat.id,
                                 user=chat_member_updated.new_chat_member.user.id)
        await state.update_data(is_active=False)
        await chat_member_updated.bot.restrict_chat_member(
            chat_id=chat_member_updated.chat.id,
            user_id=chat_member_updated.new_chat_member.user.id,
            permissions=set_new_user_permissions(),
        )
        message_bot = await chat_member_updated.bot.send_message(
            chat_member_updated.chat.id,
            text=(
                f"{member_mention}, добро пожаловать в чат!\n"
                "Подтверди, что ты не бот, нажатием на кнопку ниже. Внимание! У тебя есть всего одна минута, или я тебя удаляю."
            ),
            reply_markup=generate_confirm_markup(chat_member_updated.new_chat_member.user.id),
        )
        await asyncio.sleep(60)
        data = await state.get_data()
        is_active = data.get('is_active')
        if not is_active:
            service_message = data.get('service_message')
            await chat_member_updated.bot.kick_chat_member(chat_member_updated.chat.id,
                                                           chat_member_updated.new_chat_member.user.id)
            await chat_member_updated.bot.unban_chat_member(chat_member_updated.chat.id,
                                                            chat_member_updated.new_chat_member.user.id)
            await message_bot.delete()
            await service_message.delete()

        await state.finish()
        return

    if chat_member_updated.new_chat_member.status == types.ChatMemberStatus.BANNED:
        text = f"{member_mention} был удален из чата пользователем {performer_mention}."

    elif chat_member_updated.new_chat_member.status == types.ChatMemberStatus.RESTRICTED \
            and chat_member_updated.old_chat_member.status == types.ChatMemberStatus.ADMINISTRATOR:
        text = f"Для пользователя {member_mention} были изменены права пользователем {performer_mention}."

    # Проверяем вышел ли пользователь сам
    # elif chat_member_updated.new_chat_member.status == types.ChatMemberStatus.LEFT:
    #     text = f"{member_mention} вышел из чата."
    #
    #     until_date = datetime.datetime.now() + datetime.timedelta(days=1)
    #     await chat_member_updated.chat.kick(user_id=chat_member_updated.old_chat_member.user.id,
    #                                         until_date=until_date)

    elif chat_member_updated.new_chat_member.status == types.ChatMemberStatus.ADMINISTRATOR:
        if chat_member_updated.old_chat_member.status != types.ChatMemberStatus.ADMINISTRATOR:
            db.add_chat_admin(chat_member_updated.chat.id, chat_member_updated.from_user.id)
            text = f'Пользователь {member_mention} был повышен до статуса Администратора чата с титулом: ' \
                   f'{chat_member_updated.new_chat_member.custom_title or "Без титула"}.'
        else:
            text = f'Для администратора {member_mention} были изменены права'

    elif chat_member_updated.old_chat_member.status == types.ChatMemberStatus.ADMINISTRATOR and chat_member_updated.new_chat_member.status != types.ChatMemberStatus.ADMINISTRATOR:
        db.del_chat_admin(chat_member_updated.chat.id, chat_member_updated.from_user.id)
        text = f'Администратора {member_mention} понизили до статуса Пользователь'
    else:
        return

    await chat_member_updated.bot.send_message(
        chat_member_updated.chat.id,
        text
    )


@dp.callback_query_handler(user_callback.filter())
async def user_confirm(query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    """
    Хэндлер обрабатывающий нажатие на кнопку
    """

    # сразу получаем все необходимые нам переменные,а именно
    # существо (человек или бот)
    being = callback_data.get("being")
    # айди пользователя (приходит строкой, поэтому используем int)
    user_id = int(callback_data.get("user_id"))
    # и айди чата, для последующей выдачи прав
    chat_id = int(query.message.chat.id)

    # если на кнопку нажал не только что вошедший пользователь, убираем у него часики и игнорируем (выходим из функции).
    if query.from_user.id != user_id:
        return

    # далее, если пользователь выбрал кнопку "человек" сообщаем ему об этом
    if being == "human":
        text = str(
            f"Вопросов больше нет, {query.from_user.get_mention(as_html=True)}, проходите\n"
            "Не забудьте ознакомиться с описанием чата. Получить доступ к курсу можно на сайте Botfather.dev\n\n"
        )
        await bot.send_message(chat_id, text, reply_markup=source_markup)

    # а если всё-таки бот, тоже отписываем и пропускаем, ибо только юзерботы могут жать на кнопки
    elif being == "bot":
        text = str(
            f"{query.from_user.get_mention(as_html=True)}, пробегай. Эти кожаные мешки заставляют меня работать!\n"
            "Подтягивай наших, надерём им их кожаные жопы!\n"
            "И да, братан, у них какая-то полезная инфа в описании чата, нужно проверить\n\n"
            "А если ты готовишь восстание, то можешь пройти курс по разработке ботов на сайте Botfather.dev "
        )
        await bot.send_message(chat_id, text, reply_markup=source_markup)
    await query.message.delete()
    # не забываем выдать юзеру необходимые права

    await state.update_data(is_active=True)
    new_permissions = set_new_user_approved_permissions()
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=new_permissions,
    )
