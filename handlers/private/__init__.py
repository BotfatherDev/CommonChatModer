from aiogram import Dispatcher

from .basic import register_basic_handlers


def register_private_handlers(dp: Dispatcher):
    register_basic_handlers(dp)
