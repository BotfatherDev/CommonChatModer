from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


@dataclass
class ReplyMsgIsChannelFilter(BoundFilter):
    """
    Фильтр, проверяющий, что реплай сообщение написано от имени канала (в чате)
    """

    key = "reply_msg_is_channel"
    reply_msg_is_channel: bool

    async def check(self, message: types.Message) -> bool:
        reply = message.reply_to_message

        if not reply:
            return False
        if not reply.sender_chat:
            return False

        return reply.is_automatic_forward is None and reply.sender_chat.id != message.chat.id
