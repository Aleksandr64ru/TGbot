import feedparser
from datetime import datetime
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("news"))
async def handle_news(message: Message):
    url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
    feed = feedparser.parse(url)

    text = "📰 <b>Свежие крипто-новости</b>\n\n"

    for i, entry in enumerate(feed.entries[:5], start=1):
        title = entry.title.strip()
        link = entry.link

        # 📅 дата (если есть)
        try:
            published = entry.published
            date = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %z")
            date_str = date.strftime("%d.%m %H:%M")
        except:
            date_str = "—"

        # ✂️ обрезка длинных заголовков
        if len(title) > 80:
            title = title[:77] + "..."

        text += (
            f"{i}. <a href='{link}'>{title}</a>\n"
            f"   📅 {date_str}\n\n"
        )

    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)