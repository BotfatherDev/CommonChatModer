from aiogram import Dispatcher

from .group_chat import IsGroup


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsGroup)
