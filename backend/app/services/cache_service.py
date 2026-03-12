from app.core.config import settings


class CacheService:
    """File path cache. Uses Redis if available, otherwise in-memory dict."""

    _memory_cache: dict[str, str] = {}

    def __init__(self):
        self._redis = None

    async def _get_redis(self):
        if not settings.redis_url:
            return None
        if self._redis is None:
            import redis.asyncio as aioredis
            self._redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        return self._redis

    async def get(self, track_id: str, quality: str) -> str | None:
        key = f"file:{track_id}:{quality}"
        r = await self._get_redis()
        if r:
            return await r.get(key)
        return self._memory_cache.get(key)

    async def set(self, track_id: str, quality: str, file_path: str) -> None:
        key = f"file:{track_id}:{quality}"
        r = await self._get_redis()
        if r:
            ttl = settings.cache_ttl_hours * 3600
            await r.set(key, file_path, ex=ttl)
        else:
            self._memory_cache[key] = file_path
