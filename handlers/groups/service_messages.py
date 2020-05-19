import datetime

from aiogram import types

from filters import IsGroup
from loader import dp

from keyboards.inline import generate_confirm_markup, user_callback

from loader import bot

from data.permissions import new_user_added, user_allowed


@dp.message_handler(IsGroup(), content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def left_chat_member(message: types.Message):
    """Хендлер для вышедших либо кикнутых пользователей"""

    # TODO: Можно дёрнуть getChatMember на этот ID. Вернётся тип ChatMember с полем status.
    #  Это поле может принимать разные, значения, есть отдельно left, отдельно kicked
    #  А left_chat_member в Message в какой-то момент перестанет появляться вообще
    #  (спасибо челу из чата аиограма)

    # Если пользователя удалил бот, то это было сделано через /ban - пропускаем
    bot_me = await message.bot.get_me()
    if message.from_user.id == bot_me.id:
        return False

    # Проверяем вышел ли пользователь сам
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} вышел из чата.")

    else:
        await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} был удален из чата "
                             f"пользователем {message.from_user.get_mention(as_html=True)}.")


@dp.message_handler(IsGroup(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def new_chat_member(message: types.Message):
    """
    Обрабатываем вход нового пользователя
    """
    # Пропускаем старые запросы
    if message.date < datetime.datetime.now() - datetime.timedelta(minutes=1):
        return False

    # сразу выдаём ему права, неподтверждённого пользователя
    await bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.new_chat_members[0].id,
        permissions=new_user_added,
    )

    # TODO вместо кучи сообщений, отправлять одно с несколькими айдишниками
    
    # Каждому пользователю отсылаем кнопку
    for new_member in message.new_chat_members:
        await message.reply(
            (
                f"{new_member.get_mention(as_html=True)}, добро пожаловать в чат!\n"
                "Подтверди, что ты не бот, нажатием на кнопку ниже"
            ),
            reply_markup=generate_confirm_markup(new_member.id)
        )


@dp.callback_query_handler(user_callback.filter())
async def user_confirm(query: types.CallbackQuery, callback_data: dict):
    """
    Хэндлер обрабатывающий нажатие на кнопку
    """

    # сразу получаем все необходимые нам переменные,а именно
    # существо (человек или бот)
    being = callback_data.get("being")
    # айди пользователя (приходит строкой, поэтому используем int)
    user_id = int(callback_data.get("user_id"))
    # и айди чата, для последнующей выдачи прав
    chat_id = int(query.message.chat.id)

    # если на кнопку нажал не только что вошедший пользователь, убираем у него часики и игнорируем (выходим из функции).
    if query.from_user.id != user_id:
        await query.answer()
        return

    # далее, если пользователь выбрал кнопку "человек" сообщаем ему об этом
    if being == "human":
        text = str(
            f"Вопросов больше нет, {query.from_user.get_mention(as_html=True)}, проходите"
        )
        await bot.send_message(chat_id, text)

    # а если всё-таки бот, тоже отписываем и пропускаем, ибо только юзерботы могут жать на кнопки
    elif being == "bot":
        text = str(
            f"{query.from_user.get_mention(as_html=True)}, пробегай. Эти кожаные мешки заставляют меня работать!\n"
            "Подтягивай наших, надерём им их кожаные жопы!"
        )
        await bot.send_message(chat_id, text)

    # не забываем выдать юзеру необходимые права
    await bot.restrict_chat_member(
        chat_id=chat_id,
        user_id=user_id,
        permissions=user_allowed,
    )

    # и убираем часики
    await query.answer()

    # а также удаляем сообщение, чтобы пользователь в RO не мог получить права
    await query.message.delete()
