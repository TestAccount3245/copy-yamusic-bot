# Python Production Project Structure

This document defines best practices for organizing scalable Python projects.

The goal is:

- maintainability
- scalability
- testability
- clean architecture

---

# 1. Core Principles

A good Python project should:

- separate business logic from interfaces
- avoid large monolithic files
- use clear module boundaries
- include documentation and tests

Never mix:

- API logic
- business logic
- database logic
- bot handlers

---

# 2. Recommended Directory Layout

Example structure:


project-root/

app/
api/
services/
models/
schemas/
repositories/

bot/
handlers/
keyboards/
middlewares/

core/
config.py
logging.py
security.py

database/
models/
migrations/

miniapp/
frontend/

downloads/
cache/

tests/

docs/

scripts/

README.md
pyproject.toml
docker-compose.yml
.env.example


---

# 3. Module Responsibilities

### API

Handles HTTP requests.

Example:


api/routes/search.py
api/routes/tracks.py


Should only:

- validate input
- call services
- return responses

---

### Services

Contains business logic.

Example:


services/music_service.py
services/download_service.py
services/search_service.py


---

### Repositories

Responsible for database operations.

Example:


repositories/user_repository.py
repositories/track_repository.py


---

### Models

Database models.

Example:


models/user.py
models/track.py
models/album.py


---

### Schemas

Pydantic models for validation.

Example:


schemas/track.py
schemas/user.py


---

# 4. Configuration

All configuration must be centralized.

Example:


core/config.py


Use:

Pydantic Settings or dotenv.

Never hardcode secrets.

---

# 5. Logging

Use structured logging.

Example:


core/logging.py


Recommended libraries:

- logging
- structlog
- loguru

---

# 6. Async First

Modern Python backends should use async.

Recommended stack:

FastAPI
asyncpg
aiohttp
aiogram

---

# 7. Dependency Management

Use:


pyproject.toml


Example tools:

poetry
uv
pip-tools

---

# 8. Environment Variables

Use `.env` files.

Example:


BOT_TOKEN=
DATABASE_URL=
REDIS_URL=
YANDEX_TOKEN=


Include `.env.example` in repository.

---

# 9. Testing

Tests must exist in `/tests`.

Example structure:


tests/
test_api.py
test_services.py
test_bot.py


Use:

pytest

---

# 10. Documentation

Every production repository should include:

README.md
docs/ folder

Documentation should explain:

- architecture
- setup
- environment variables
- deployment

---

# 11. Containerization

Use Docker.

Example files:


Dockerfile
docker-compose.yml


Services:

- API
- bot
- database
- redis

---

# 12. Code Style

Use:

black
ruff
isort
mypy

Example config:


pyproject.toml


---

# 13. GitHub Best Practices

Repository should include:

README.md
LICENSE
CONTRIBUTING.md
.env.example

Optional:

GitHub Actions CI

---

# 14. Example Service Layer

Example:

```python
class TrackService:

    def __init__(self, yandex_client):
        self.client = yandex_client

    async def get_track(self, track_id: int):
        return await self.client.tracks(track_id)
15. Avoid These Mistakes

Do NOT:

write 2000-line files

mix bot + API code

store business logic in handlers

ignore error handling

16. Scalability Strategy

Structure should allow easy addition of:

new APIs

new services

new integrations

microservices in future

Conclusion

A well-structured Python project enables:

fast development

easier debugging

community contributions

long-term maintenance