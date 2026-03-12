from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data.startswith("dl:"))
async def handle_download(callback: CallbackQuery) -> None:
    # Format: dl:{track_id}:{quality}
    parts = callback.data.split(":") if callback.data else []
    if len(parts) < 3:
        await callback.answer("Invalid download request")
        return

    track_id = parts[1]
    quality = parts[2]

    await callback.answer("Downloading...")
    # TODO: call download service, send audio file
    await callback.message.answer(f"Downloading track {track_id} in {quality}...")  # type: ignore
