from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["tracks"])


class DownloadRequest(BaseModel):
    quality: str = "mp3"


@router.get("/tracks/{track_id}")
async def get_track(track_id: str, user: User = Depends(get_current_user)) -> dict:
    from app.services.yandex_music import YandexMusicService

    service = YandexMusicService(user.yandex_token)
    track = await service.get_track(track_id)
    return {"track": track}


@router.post("/tracks/{track_id}/download")
async def download_track(
    track_id: str,
    body: DownloadRequest,
    user: User = Depends(get_current_user),
) -> dict:
    from app.services.download_service import DownloadService

    service = DownloadService()
    result = await service.download_track(
        track_id=track_id, quality=body.quality, user=user
    )
    return {"status": "sent", "file_size": result.get("file_size")}
