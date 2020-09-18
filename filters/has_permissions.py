import logging
import typing
from dataclasses import dataclass

import loguru
from aiogram import types
from aiogram.dispatcher.filters import Filter, BoundFilter


@dataclass
class HasPermissions(Filter):
    """
    Проверяет, есть ли у пользователя необходимые права
    """

    can_post_messages: bool = False
    can_edit_messages: bool = False
    can_delete_messages: bool = False
    can_restrict_members: bool = False
    can_promote_members: bool = False
    can_change_info: bool = False
    can_invite_users: bool = False
    can_pin_messages: bool = False

    ARGUMENTS = {
        "user_can_post_messages": "can_post_messages",
        "user_can_edit_messages": "can_edit_messages",
        "user_can_delete_messages": "can_delete_messages",
        "user_can_restrict_members": "can_restrict_members",
        "user_can_promote_members": "can_promote_members",
        "user_can_change_info": "can_change_info",
        "user_can_invite_users": "can_invite_users",
        "user_can_pin_messages": "can_pin_messages",
    }
    PAYLOAD_ARGUMENT_NAME = "user_member"

    def __post_init__(self):
        """
        Генерирует словарь вида permission: bool, чтобы знать, какие значения переданы в фильтр

        Пример итогового словаря:
        required_permissions = {
            can_edit_messages: True,
            can_restrict_members: True
        }

        """
        self.required_permissions = {
            arg: True for arg in self.ARGUMENTS.values() if getattr(self, arg)
        }

    @classmethod
    def validate(
        cls, full_config: typing.Dict[str, typing.Any]
    ) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """
        Метод, необходимый для использования фильтра из filters_factory
        """
        config = dict()
        for alias, argument in cls.ARGUMENTS.items():
            if alias in full_config:
                config[argument] = full_config.pop(alias)
        return config

    def _get_cached_value(self, message: types.Message) -> typing.Optional[types.ChatMember]:
        """
        Метод, для получения сохранённого в кеше пользователя

        возвращает None, если пользователь не в кеше
        """
        try:
            return message.conf[self.PAYLOAD_ARGUMENT_NAME]
        except KeyError:
            return None

    def _set_cached_value(self, message: types.Message, member: types.ChatMember):
        """
        Добавляет в кеш пользователя
        """
        message.conf[self.PAYLOAD_ARGUMENT_NAME] = member

    async def _get_chat_member(self, message: types.Message) -> typing.Union[bool, types.ChatMember]:
        """
        Метод для получения пользователя
        Если пользователь сохранён в кеше, достаёт пользователя из кеша и возвращает
        В противном случае делает запрос телеграму, сохраняя результат в кеш
        """
        chat_member: types.ChatMember = self._get_cached_value(message)
        if chat_member is None:
            admins = await message.chat.get_administrators()
            target_user_id = await self.get_target_id(message)
            try:
                chat_member = next(filter(lambda member: member.user.id == target_user_id, admins))

            except StopIteration:
                return False
            self._set_cached_value(message, chat_member)
        return chat_member

    async def check(
        self, message: types.Message
    ) -> bool:
        """
        Основная логика фильтра. Возвращает True/False, или словарь с пользователем
        Когда возвращается False, бот не проваливается в handler
        """
        chat_member = await self._get_chat_member(message)
        if not chat_member:
            return False
        if chat_member.status == types.ChatMemberStatus.CREATOR:
            return chat_member

        for permission, value in self.required_permissions.items():

            if not getattr(chat_member, permission):
                return False
        return True

    async def get_target_id(self, message: types.Message) -> int:
        """
        Возвращает айди пользователя, отправившего сообщение (Создано для уменьшения количества кода)
        """
        return message.from_user.id
