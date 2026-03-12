from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Telegram
    bot_token: str
    miniapp_url: str = "https://localhost:3000"

    # CORS — дополнительные origins для GitHub Pages и tunnel
    cors_origins: str = ""  # comma-separated, e.g. "https://user.github.io,https://xxx.trycloudflare.com"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/yamusic"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Storage
    upload_max_size_mb: int = 50
    storage_path: str = "storage"
    cache_ttl_hours: int = 24

    # Rate limits
    downloads_per_hour: int = 30
    uploads_per_day: int = 10

    # Security
    api_key_header: str = "X-API-Key"

    @property
    def upload_max_size_bytes(self) -> int:
        return self.upload_max_size_mb * 1024 * 1024


settings = Settings()  # type: ignore[call-arg]
