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

        if not isinstance(data, list):
            await message.answer("❌ Ошибка API, попробуй позже")
            return

        text = "📊 Топ-10 криптовалют:\n\n"

        for i, coin in enumerate(data, start=1):
            name = coin["name"]
            symbol = coin["symbol"].upper()
            price = round(coin["current_price"], 2)
            change = coin.get("price_change_percentage_24h", 0)

            trend = "🟢" if change >= 0 else "🔴"

            text += f"{i}. {name} ({symbol}) — 💰 {price} USDT {trend} {change:.2f}%\n"

        await message.answer(text)

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")