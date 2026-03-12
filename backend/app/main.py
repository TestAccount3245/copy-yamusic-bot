from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging()

    # Redis is optional for dev mode
    if settings.redis_url:
        import redis.asyncio as aioredis
        app.state.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    else:
        app.state.redis = None

    yield

    if app.state.redis:
        await app.state.redis.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="YaMusic Bot API",
        version="0.1.0",
        lifespan=lifespan,
    )

    origins = [settings.miniapp_url, "http://localhost:3000"]
    if settings.cors_origins:
        origins.extend(o.strip() for o in settings.cors_origins.split(",") if o.strip())

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.api.routes import search, tracks, albums, artists, wave, uploads, users

    app.include_router(search.router, prefix="/api")
    app.include_router(tracks.router, prefix="/api")
    app.include_router(albums.router, prefix="/api")
    app.include_router(artists.router, prefix="/api")
    app.include_router(wave.router, prefix="/api")
    app.include_router(uploads.router, prefix="/api")
    app.include_router(users.router, prefix="/api")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
