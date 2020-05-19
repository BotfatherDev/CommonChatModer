from aiogram import types

# Права пользователя, только вошедшего в чат
new_user_added = types.ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_invite_users=False,
    can_change_info=False,
    can_pin_messages=False,
)

# Права пользователя, подтвердившего, что он не бот
user_allowed = types.ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_invite_users=True,
    can_change_info=False,
    can_pin_messages=False,
)

# Права пользователя в муте
user_ro = types.ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_invite_users=True,
    can_change_info=False,
    can_pin_messages=False,
)
