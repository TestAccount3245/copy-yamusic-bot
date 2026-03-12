import hashlib
import hmac
from urllib.parse import parse_qs, unquote

from app.core.config import settings


def verify_init_data(init_data: str) -> dict:
    """Verify Telegram WebApp initData HMAC-SHA256 signature.

    See: https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    parsed = parse_qs(init_data, keep_blank_values=True)

    if "hash" not in parsed:
        raise ValueError("Missing hash")

    received_hash = parsed.pop("hash")[0]

    data_check_string = "\n".join(
        f"{k}={unquote(v[0])}" for k, v in sorted(parsed.items())
    )

    secret_key = hmac.new(
        b"WebAppData",
        settings.bot_token.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    computed_hash = hmac.new(
        secret_key,
        data_check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(computed_hash, received_hash):
        raise ValueError("Invalid hash")

    return parsed
