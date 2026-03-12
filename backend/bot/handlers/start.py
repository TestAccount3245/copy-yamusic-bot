from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

from app.core.config import settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    text = (
        "Welcome to YaMusic Bot!\n\n"
        "Or use /search QUERY for quick search.\n"
        "Use /link TOKEN to connect your Yandex Music account."
    )

    if settings.miniapp_url.startswith("https://"):
        button = InlineKeyboardButton(
            text="🎵 Open Music App",
            web_app=WebAppInfo(url=settings.miniapp_url),
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])
        text = (
            "Welcome to YaMusic Bot!\n\n"
            "Open the Mini App to search, browse, and download music.\n"
            "Or use /search QUERY for quick search.\n"
            "Use /link TOKEN to connect your Yandex Music account."
        )
        await message.answer(text, reply_markup=keyboard)
    else:
        # Dev mode: no valid HTTPS URL, skip WebApp button
        await message.answer(text)
