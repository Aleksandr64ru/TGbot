import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command


BOT_TOKEN = "8787403562:AAGGv750U61jl9jzEwn9FfnREOZPnir4BEI"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Hello!")
    
async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())