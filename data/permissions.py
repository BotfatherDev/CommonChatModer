from aiogram import types
from loguru import logger
from copy import copy

default_permissions = {'can_send_messages': True,
                       'can_send_media_messages': True,
                       'can_send_polls': True,
                       'can_send_other_messages': True,
                       'can_add_web_page_previews': True,
                       'can_invite_users': True,
                       'can_change_info': False,
                       'can_pin_messages': False
                       }


# Права пользователя, только вошедшего в чат
def set_new_user_permissions():
    new_permissions = copy(default_permissions)
    new_permissions.update(
        can_send_messages=False,
        can_send_media_messages=False,
    )
    return types.ChatPermissions(
        **new_permissions
    )


# Права пользователя, подтвердившего, что он не бот
def set_new_user_approved_permissions():
    return types.ChatPermissions(
        **default_permissions
    )


# Права пользователя в муте
def set_user_ro_permissions():
    new_permissions = copy(default_permissions)
    new_permissions.update(
        can_send_messages=False,
    )
    return types.ChatPermissions(
        **new_permissions
    )


def set_no_media_permissions():
    new_permissions = copy(default_permissions)
    new_permissions.update(
        can_send_media_messages=False,
    )
    return types.ChatPermissions(
        **new_permissions
    )
