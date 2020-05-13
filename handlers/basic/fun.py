import re
from random import randint

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("gay", prefixes="!/"))
async def gay(message: types.Message):
    command_parse = re.compile(r"(!gay|/gay) ?(\w+)?")
    parsed = command_parse.match(message.text)

    target = parsed.group(2)
    percentage = randint(0, 100)

    if not target:
        target = message.from_user.get_mention()

    await message.reply(f"🏳️‍🌈 Похоже, что {target} гей на {percentage}%")
