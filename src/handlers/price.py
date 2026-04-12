import aiohttp
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


# 📈 ASCII-график
def generate_chart(prices: list) -> str:
    blocks = "▁▂▃▄▅▆▇█"

    min_price = min(prices)
    max_price = max(prices)

    if max_price == min_price:
        return "—" * len(prices)

    chart = ""
    for price in prices:
        normalized = (price - min_price) / (max_price - min_price)
        index = int(normalized * (len(blocks) - 1))
        chart += blocks[index]

    return chart


@router.message(Command("price"))
async def handle_price(message: Message):
    try:
        parts = message.text.split()

        if len(parts) < 2:
            await message.answer("❗ Используй: /price BTC")
            return

        query = parts[1].lower()

        async with aiohttp.ClientSession() as session:

            # 🔍 поиск монеты
            search_url = "https://api.coingecko.com/api/v3/search"
            async with session.get(search_url, params={"query": query}) as resp:
                search_data = await resp.json()

            coins = search_data.get("coins", [])

            if not coins:
                await message.answer("❌ Монета не найдена")
                return

            coin_id = coins[0]["id"]

            # 💰 данные по цене
            market_url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "ids": coin_id,
                "price_change_percentage": "24h"
            }

            async with session.get(market_url, params=params) as resp:
                data = await resp.json()

            if not data:
                await message.answer("❌ Не удалось получить данные")
                return

            coin = data[0]

            name = coin["name"]
            symbol = coin["symbol"].upper()
            price = round(coin["current_price"], 2)
            change = coin.get("price_change_percentage_24h", 0)
            market_cap = coin.get("market_cap", 0)

            trend = "🟢" if change >= 0 else "🔴"

            # 💰 формат капитализации
            if market_cap >= 1_000_000_000:
                cap = f"{round(market_cap / 1_000_000_000, 2)}B$"
            elif market_cap >= 1_000_000:
                cap = f"{round(market_cap / 1_000_000, 2)}M$"
            else:
                cap = f"{market_cap}$"

            # 📉 получаем историю (24 часа)
            chart_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": 1
            }

            async with session.get(chart_url, params=params) as resp:
                chart_data = await resp.json()

            prices = [point[1] for point in chart_data["prices"]]

            # уменьшаем длину графика
            prices = prices[-20:]

            chart = generate_chart(prices)

        # 📤 итоговый текст
        text = (
            f"💰 <b>{name} ({symbol})</b>\n\n"
            f"Цена: {price} USDT\n"
            f"Изменение: {trend} {change:.2f}%\n"
            f"Капитализация: {cap}\n\n"
            f"📈 <b>24ч график:</b>\n"
            f"<code>{chart}</code>"
        )

        await message.answer(text, parse_mode="HTML")

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")