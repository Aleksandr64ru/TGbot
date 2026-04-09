from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def handle_start(message: Message):
    text = (
        "👋 Добро пожаловать в крипто-бота!\n\n"
        "📌 Доступные команды:\n\n"
        "/top — 📊 Топ-10 криптовалют\n"
        "/news — 📊 Последние новости о крипте\n"
    )

    await message.answer(text)