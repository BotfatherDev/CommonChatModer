from aiogram import Dispatcher

from .errors import register_errors_handler
from .metabolism import register_metabolism_handlers
from .other import register_other_handlers


def register_essential_handlers(dp: Dispatcher):
    register_errors_handler(dp)
    register_metabolism_handlers(dp)
    register_other_handlers(dp)
