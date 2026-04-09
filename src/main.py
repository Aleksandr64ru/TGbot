import os
import json
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Update

# 👇 подключаем роутеры
from handlers.start import router as start_router
from handlers.top import router as top_router
# from handlers.news import router as news_router


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 👇 регистрируем все роутеры
dp.include_router(start_router)
dp.include_router(top_router)
# dp.include_router(news_router)


async def handler(event: dict, context):
    body: str = event["body"]
    update_data = json.loads(body) if body else {}

    await dp.feed_update(
        bot,
        Update.model_validate(update_data),
    )

    return {"statusCode": 200, "body": "fine"}


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())