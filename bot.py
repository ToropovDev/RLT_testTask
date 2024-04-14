import os
from aiogram import types, Bot, Dispatcher
from aiogram.filters.command import CommandStart, Command
import dotenv

dotenv.load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def start_bot():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет! Пришли свой запрос!")


@dp.message()
async def on_message(message):
    await message.answer(message.text)
