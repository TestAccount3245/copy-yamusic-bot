from app.core.logging import get_logger

logger = get_logger(__name__)


class UserService:
    async def link_yandex_token(self, user_id: int, token: str) -> None:
        """Save user's Yandex OAuth token."""
        # TODO: validate token by trying to init YandexMusicService
        # TODO: encrypt and store in DB
        logger.info("Yandex token linked", user_id=user_id)

    async def update_settings(self, user_id: int, **kwargs) -> None:
        """Update user preferences."""
        # TODO: update in DB
        logger.info("Settings updated", user_id=user_id, **kwargs)

    async def get_or_create(self, telegram_id: int, username: str | None, first_name: str | None) -> dict:
        """Get existing user or create new one."""
        # TODO: upsert in DB
        return {
            "id": telegram_id,
            "username": username,
            "first_name": first_name,
        }
