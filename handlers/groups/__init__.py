from aiogram import Dispatcher

from .basic import register_basic_handlers
from .casino import register_casino_handlers
from .edit_chat import register_edit_chat_handlers
from .group_approval import register_group_approval
from .moderate_chat import register_moderate_chat_handlers
from .rating import register_ratng_handlers
from .report import register_report_handlers
from .service_messages import register_service_handlers


def register_group_handlers(dp: Dispatcher):
    """
    Регистрация всех хэндлеров
    """
    register_basic_handlers(dp)
    register_casino_handlers(dp)
    register_edit_chat_handlers(dp)
    register_moderate_chat_handlers(dp)
    register_ratng_handlers(dp)
    register_report_handlers(dp)
    register_service_handlers(dp)
    register_group_approval(dp)
