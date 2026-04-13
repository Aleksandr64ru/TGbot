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
            async with session.get(url, timeout=10) as resp:
                data = await resp.text()

        # 🛡 защита от пустого ответа
        if not data:
            await message.answer("❌ Не удалось получить новости")
            return

        # 📦 парсинг XML
        try:
            root = ET.fromstring(data)
        except ET.ParseError:
            await message.answer("❌ Ошибка парсинга новостей")
            return

        items = root.findall(".//item")

        if not items:
            await message.answer("❌ Новости не найдены")
            return

        text = "📰 <b>Свежие крипто-новости</b>\n\n"

        for i, item in enumerate(items[:5], start=1):

            title_elem = item.find("title")
            link_elem = item.find("link")

            title = title_elem.text if title_elem is not None and title_elem.text else "Без заголовка"
            link = link_elem.text if link_elem is not None and link_elem.text else "#"

            text += f"{i}. <a href='{link}'>{title}</a>\n"

        await message.answer(
            text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        await message.answer("❌ Ошибка при получении новостей")
        print(f"[NEWS ERROR]: {e}")