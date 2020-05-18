from aiogram import Dispatcher

from .group_chat import IsGroup
from .private_chat import IsPrivate

def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
