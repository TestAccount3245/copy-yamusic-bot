from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup

from app.core.config import settings

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎵 Open Music App",
                    web_app=WebAppInfo(url=settings.miniapp_url),
                )
            ]
        ]
    )
    await message.answer(
        "Welcome to YaMusic Bot!\n\n"
        "Open the Mini App to search, browse, and download music.\n"
        "Or use /search <query> for quick search.\n"
        "Use /link <token> to connect your Yandex Music account.",
        reply_markup=keyboard,
    )
