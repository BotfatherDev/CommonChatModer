from aiogram import Dispatcher

from .user_filters import IsContributor
from .chat_filters import IsGroup, IsPrivate


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsContributor)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
