import os
import json

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import Command


BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def handle_start(message: Message):
    await message.answer("Hello!")
    
async def handler(event: dict, context):
    body: str = event["body"]
    update_data = json.loads(body) if body else {}
    await dp.feed_update(
        bot,
        Update.model_validate{update_data},
    )
    
    
    return{"statusCode": 200, "body": "fine"}  
    
    
async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())