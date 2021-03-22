from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivateAdmin(BoundFilter):
    def __init__(self, users_id: list):
        self.users_id = list(map(int, users_id))

    async def check(self, message:types.Message):

        return message.from_user.id in self.users_id
