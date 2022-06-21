from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from loader import db


async def updated_chat_member(chat_member_updated: types.ChatMemberUpdated, state: FSMContext):
    """Хендлер для вышедших либо кикнутых пользователей"""

    performer_mention = chat_member_updated.from_user.get_mention(as_html=True)
    member_mention = chat_member_updated.old_chat_member.user.get_mention(as_html=True)

    bot_user = await chat_member_updated.bot.me
    if chat_member_updated.from_user.id == bot_user.id:
        return False

    if chat_member_updated.new_chat_member.status == types.ChatMemberStatus.MEMBER:
        # REMOVED. Now bot approves users on join request in private chat
        pass
    if chat_member_updated.new_chat_member.status == types.ChatMemberStatus.BANNED:
        text = f"{member_mention} был удален из чата пользователем {performer_mention}."

    elif chat_member_updated.new_chat_member.status == types.ChatMemberStatus.RESTRICTED \
            and chat_member_updated.old_chat_member.status == types.ChatMemberStatus.ADMINISTRATOR:
        text = f"Для пользователя {member_mention} были изменены права пользователем {performer_mention}."


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


def register_service_handlers(dp: Dispatcher):
    """
    Регистрация всех хэндлеров
    """

    dp.register_chat_member_handler(updated_chat_member)
