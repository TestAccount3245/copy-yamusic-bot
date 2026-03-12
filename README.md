# YaMusic Bot

Telegram Mini App music service based on the Yandex Music ecosystem.

## Features

- **Telegram Mini App** — modern Liquid Glass UI for browsing and downloading music
- **Telegram Bot** — quick search and download via chat commands
- **Yandex Music Integration** — search, tracks, albums, artists, My Wave
- **FLAC Support** — lossless audio download with quality selection
- **Custom Uploads** — upload and share your own tracks with other users
- **Public API** — REST endpoints for third-party integration

## Architecture

```
backend/     Python (FastAPI + aiogram + yandex-music-api)
miniapp/     React + TypeScript + Tailwind CSS
nginx/       Reverse proxy configuration
```

## Quick Start

```bash
# 1. Copy environment config
cp .env.example .env
# Edit .env with your BOT_TOKEN and other settings

# 2. Start all services
docker compose up --build

# 3. Run database migrations
docker compose exec backend alembic upgrade head
```

## Bot Commands

- `/start` — Open the Mini App
- `/search <query>` — Quick search
- `/link <token>` — Connect your Yandex Music account
- `/settings` — View settings

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/search?q=&type=` | Unified search |
| GET | `/api/tracks/{id}` | Track details |
| GET | `/api/albums/{id}` | Album with tracks |
| GET | `/api/artists/{id}` | Artist info |
| POST | `/api/tracks/{id}/download` | Download track |
| POST | `/api/albums/{id}/download` | Download album |
| GET | `/api/wave` | My Wave feed |
| POST | `/api/uploads` | Upload custom track |
| GET | `/api/uploads` | List uploaded tracks |
| GET | `/api/users/me` | Current user |

## Tech Stack

- **Backend**: Python 3.11, FastAPI, aiogram 3, SQLAlchemy 2, asyncpg
- **Music API**: yandex-music (unofficial)
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Zustand
- **Database**: PostgreSQL 16, Redis 7
- **Deploy**: Docker Compose, nginx

## License

MIT
