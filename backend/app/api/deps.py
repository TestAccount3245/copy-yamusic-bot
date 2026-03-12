import hashlib
import hmac
from urllib.parse import parse_qs, unquote

from fastapi import Depends, Request

from app.core.config import settings
from app.core.exceptions import AuthError
from app.models.user import User


def verify_telegram_init_data(init_data: str) -> dict:
    """Verify Telegram Mini App initData using HMAC-SHA256."""
    parsed = parse_qs(init_data)

    if "hash" not in parsed:
        raise AuthError("Missing hash in initData")

    received_hash = parsed.pop("hash")[0]

    data_check_string = "\n".join(
        f"{k}={unquote(v[0])}" for k, v in sorted(parsed.items())
    )

    secret_key = hmac.new(
        b"WebAppData", settings.bot_token.encode(), hashlib.sha256
    ).digest()

    computed_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise AuthError("Invalid initData signature")

    return parsed


async def get_current_user(request: Request) -> User:
    """Extract user from Telegram initData header or API key."""
    init_data = request.headers.get("X-Telegram-Init-Data")
    api_key = request.headers.get(settings.api_key_header)

    if init_data:
        import json

        data = verify_telegram_init_data(init_data)
        if "user" in data:
            user_data = json.loads(unquote(data["user"][0]))
            user = User(
                id=user_data["id"],
                username=user_data.get("username"),
                first_name=user_data.get("first_name"),
            )
            # TODO: upsert user in DB, fetch full record with yandex_token
            return user

    if api_key:
        # TODO: look up user by api_key in DB
        raise AuthError("API key auth not yet implemented")

    raise AuthError("No authentication provided")
