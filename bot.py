from aiogram import types, Bot, Dispatcher
from aiogram.filters.command import CommandStart
from db import get_response
import logging
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def start_bot() -> None:
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def start(message: types.Message) -> None:
    name = f"<a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
    await message.answer(f"Hi {name}!", parse_mode='HTML')


@dp.message()
async def on_message(message: types.Message) -> None:
    request = eval(message.text)
    response = get_response(request)
    await message.answer(response)

