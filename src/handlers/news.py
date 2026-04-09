import aiohttp
import xml.etree.ElementTree as ET
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("news"))
async def handle_news(message: Message):
    try:
        url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.text()

        root = ET.fromstring(data)
        items = root.findall(".//item")[:5]

        text = "📰 <b>Свежие крипто-новости</b>\n\n"

        for i, item in enumerate(items, start=1):
            title_elem = item.find("title")
            link_elem = item.find("link")

            title = title_elem.text if title_elem is not None else "Нет заголовка"
            link = link_elem.text if link_elem is not None else "#"

            text += f"{i}. <a href='{link}'>{title}</a>\n"

        await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        await message.answer(f"Ошибка при получении новостей: {e}")