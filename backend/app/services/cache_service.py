import redis.asyncio as aioredis

from app.core.config import settings


class CacheService:
    def __init__(self):
        self._redis: aioredis.Redis | None = None

    async def _get_redis(self) -> aioredis.Redis:
        if self._redis is None:
            self._redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        return self._redis

    async def get(self, track_id: str, quality: str) -> str | None:
        r = await self._get_redis()
        return await r.get(f"file:{track_id}:{quality}")

    async def set(self, track_id: str, quality: str, file_path: str) -> None:
        r = await self._get_redis()
        ttl = settings.cache_ttl_hours * 3600
        await r.set(f"file:{track_id}:{quality}", file_path, ex=ttl)
