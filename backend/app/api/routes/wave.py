from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["wave"])


@router.get("/wave")
async def get_wave(user: User = Depends(get_current_user)) -> dict:
    from app.services.yandex_music import YandexMusicService

    service = YandexMusicService(user.yandex_token)
    tracks = await service.get_wave()
    return {"tracks": tracks}
