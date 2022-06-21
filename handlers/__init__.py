from aiogram import Dispatcher

from .essential import register_essential_handlers
from .groups import register_group_handlers
from .private import register_private_handlers


def register_all_handlers(dp: Dispatcher):
    register_group_handlers(dp)
    register_essential_handlers(dp)
    register_private_handlers(dp)
