import re
from random import randint

from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp

from utils.misc.throttling import generate_num


@dp.message_handler(Command("gay", prefixes="!/"))
async def gay(message: types.Message):
    command_parse = re.compile(r"(!gay|/gay) ?(\w+)?")
    parsed = command_parse.match(message.text)

    target = parsed.group(2)
    percentage = randint(0, 100)

    if not target:
        target = message.from_user.get_mention()

    await message.reply(f"🏳️‍🌈 Похоже, что {target} гей на {percentage}%")


@dp.message_handler(Command("biba", prefixes="!/"))
async def biba(message: types.Message):
    command_parse = re.compile(r"(!biba|/biba) ?(-?\d*)?-?(\d+)?")
    parsed = command_parse.match(message.text)
    width = generate_num(parsed.group(2), parsed.group(3), 1, 30)
    if message.reply_to_message:
        target = message.reply_to_message.from_user.get_mention(as_html=True)
    else:
        target = message.from_user.get_mention(as_html=True)

    await message.reply(f"У {target} биба {width}см")


@dp.message_handler(Command("roll", prefixes="!/"))
async def roll(message: types.Message):
    command_parse = re.compile(r"(!roll|/roll) ?(-?\d*)?-?(\d+)?")
    parsed = command_parse.match(message.text)
    width = generate_num(parsed.group(2), parsed.group(3))
    await message.reply(f"Ваше число: <b>{width}</b>")

