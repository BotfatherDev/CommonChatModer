from aiogram import types
from aiogram.types import User
from loguru import logger

permission_keys = {'can_send_messages', 'can_send_media_messages', 'can_send_polls',
                   'can_send_other_messages', 'can_add_web_page_previews', 'can_invite_users',
                   'can_change_info', 'can_pin_messages'}


def update_permissions(member: User, **new_permissions):
    permissions = dict()
    for permission_key in permission_keys:
        if (permission := new_permissions.get(permission_key)) is not None:
            permissions.update({permission_key: permission})
        else:
            permission = getattr(member, permission_key)
            permissions.update({permission_key: permission})
    return permissions


# Права пользователя, только вошедшего в чат
def set_new_user_permissions(member):
    return types.ChatPermissions(
        **update_permissions(
            member=member,
            can_send_messages=False,
            can_send_media_messages=False,
        )
    )


# Права пользователя, подтвердившего, что он не бот
def set_new_user_approved_permissions(member):
    return types.ChatPermissions(
        **update_permissions(
            member,
            can_send_messages=True,
            can_send_polls=True,
        ))


# Права пользователя в муте
def set_user_ro_permissions(member):
    return types.ChatPermissions(
        **update_permissions(
            member,
            can_send_messages=False,
        ))


def set_no_media_permissions(member):
    return types.ChatPermissions(
        **update_permissions(
            member,
            can_send_media_messages=False,
        ))
