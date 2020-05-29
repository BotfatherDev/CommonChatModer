from aiogram import Dispatcher

from .group_chat import IsGroup
from .private_chat import IsPrivate
from .is_banable import IsBanable


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsBanable)
