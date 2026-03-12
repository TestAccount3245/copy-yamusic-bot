from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("link"))
async def cmd_link(message: Message) -> None:
    token = message.text.replace("/link", "", 1).strip() if message.text else ""
    if not token:
        await message.answer("Usage: /link <yandex_oauth_token>")
        return

    # TODO: save token to DB via user_service
    await message.answer("Yandex Music account linked successfully!")


@router.message(Command("settings"))
async def cmd_settings(message: Message) -> None:
    await message.answer(
        "Settings:\n"
        "• /link <token> — Link Yandex Music account\n"
        "• Quality preference can be set in the Mini App"
    )
