import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.core.config import settings
from app.core.logging import get_logger, setup_logging

logger = get_logger(__name__)


async def main() -> None:
    setup_logging()

    bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    from bot.handlers import start, search, download, settings as settings_handler

    dp.include_router(start.router)
    dp.include_router(search.router)
    dp.include_router(download.router)
    dp.include_router(settings_handler.router)

    logger.info("Bot starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
