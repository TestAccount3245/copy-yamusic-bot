from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["albums"])


class AlbumDownloadRequest(BaseModel):
    quality: str = "mp3"


@router.get("/albums/{album_id}")
async def get_album(album_id: str, user: User = Depends(get_current_user)) -> dict:
    from app.services.yandex_music import YandexMusicService

    service = YandexMusicService(user.yandex_token)
    album = await service.get_album(album_id)
    return {"album": album}


@router.post("/albums/{album_id}/download")
async def download_album(
    album_id: str,
    body: AlbumDownloadRequest,
    user: User = Depends(get_current_user),
) -> dict:
    from app.services.download_service import DownloadService

    service = DownloadService()
    result = await service.download_album(
        album_id=album_id, quality=body.quality, user=user
    )
    return {"status": "sent", "tracks_count": result.get("tracks_count")}
