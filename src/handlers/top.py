import aiohttp
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("top"))
async def handle_top(message: Message):
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"

        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 10,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                data = await resp.json()

        # 🛡 защита от API-ошибок
        if not isinstance(data, list):
            await message.answer("❌ Ошибка API, попробуй позже")
            return

        text = "📊 <b>Топ-10 криптовалют</b>\n\n"

        for i, coin in enumerate(data, start=1):

            name = coin.get("name", "Unknown")
            symbol = coin.get("symbol", "???").upper()

            price = coin.get("current_price", 0)
            price = round(price, 2)

            # 🛡 защита от None (ВАЖНО)
            change = coin.get("price_change_percentage_24h") or 0

            trend = "🟢" if change >= 0 else "🔴"

            text += (
                f"{i}. {name} ({symbol})\n"
                f"💰 {price} USDT {trend} {change:.2f}%\n\n"
            )

        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer("❌ Ошибка при получении данных. Попробуй позже.")
        print(f"[TOP ERROR]: {e}")