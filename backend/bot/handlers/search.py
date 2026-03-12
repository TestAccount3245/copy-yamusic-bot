from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

router = Router()


@router.message(Command("search"))
async def cmd_search(message: Message) -> None:
    query = message.text.replace("/search", "", 1).strip() if message.text else ""
    if not query:
        await message.answer("Usage: /search <query>")
        return

    # TODO: call search service
    await message.answer(
        f"Searching for: {query}...",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔍 Search in App", callback_data="open_app")]
            ]
        ),
    )
