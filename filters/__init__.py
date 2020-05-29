from aiogram import Dispatcher

from .user_fillters import IsContributor
from .chat_fillters import IsGroup, IsPrivate


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsContributor)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
