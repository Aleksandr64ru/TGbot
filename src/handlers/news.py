import feedparser
import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

async def get_feed():
    loop = asyncio.get_running_loop()
    # запускаем синхронный feedparser в отдельном потоке
    return await loop.run_in_executor(None, lambda: feedparser.parse("https://www.coindesk.com/arc/outboundfeeds/rss/"))

@router.message(Command("news"))
async def handle_news(message: Message):
    feed = await get_feed()  # теперь асинхронно

    text = "📰 <b>Свежие крипто-новости</b>\n\n"
    for i, entry in enumerate(feed.entries[:5], start=1):
        text += f"{i}. {entry.title}\n"
    await message.answer(text, parse_mode="HTML")