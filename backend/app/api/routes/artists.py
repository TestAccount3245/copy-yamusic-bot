from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["artists"])


@router.get("/artists/{artist_id}")
async def get_artist(artist_id: str, user: User = Depends(get_current_user)) -> dict:
    from app.services.yandex_music import YandexMusicService

    service = YandexMusicService(user.yandex_token)
    artist = await service.get_artist(artist_id)
    return {"artist": artist}


@router.post("/artists/{artist_id}/download")
async def download_artist(
    artist_id: str,
    user: User = Depends(get_current_user),
) -> dict:
    from app.services.download_service import DownloadService

    service = DownloadService()
    result = await service.download_artist(artist_id=artist_id, user=user)
    return {"status": "sent", "tracks_count": result.get("tracks_count")}
