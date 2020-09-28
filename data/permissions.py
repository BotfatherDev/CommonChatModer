from aiogram import types
from aiogram.types import User
from loguru import logger

permission_keys = {'can_send_messages', 'can_send_media_messages', 'can_send_polls',
                   'can_send_other_messages', 'can_add_web_page_previews', 'can_invite_users',
                   'can_change_info', 'can_pin_messages'}


def update_permissions(member: User, default_permissions, **new_permissions):
    permissions = dict()
    default_permissions = default_permissions.__dict__.get("_values")

    for permission_key in permission_keys:
        if (permission := new_permissions.get(permission_key)) is not None:
            # permissions.update({permission_key: None if not permission else True})
            # CAN SEND MEDIA MESSAGES TO FALSE IS NOT WORKING
            continue
        elif (permission := default_permissions.get(permission_key)) is not None:
            permissions.update({permission_key: permission})
        else:
            permission = getattr(member, permission_key)
            permissions.update({permission_key: permission})
    return permissions


# Права пользователя, только вошедшего в чат
def set_new_user_permissions(member, default_permissions):
    return types.ChatPermissions(
        **update_permissions(
            member=member,
            default_permissions=default_permissions,
            can_send_messages=False,
            can_send_media_messages=False,
        )
    )


# Права пользователя, подтвердившего, что он не бот
def set_new_user_approved_permissions(member, default_permissions):
    return types.ChatPermissions(
        **update_permissions(
            member,
            default_permissions=default_permissions,
            can_send_messages=True,
            can_send_polls=True,
        )
    )


# Права пользователя в муте
def set_user_ro_permissions(member, default_permissions):
    return types.ChatPermissions(
        **update_permissions(
            member,
            default_permissions=default_permissions,
            can_send_messages=False,
        )
    )


def set_no_media_permissions(member, default_permissions):
    return types.ChatPermissions(
        **update_permissions(
            member,
            default_permissions=default_permissions,
            can_send_media_messages=False,
        )
    )
