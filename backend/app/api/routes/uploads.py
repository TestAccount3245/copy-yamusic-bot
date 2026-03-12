from fastapi import APIRouter, Depends, Query, UploadFile
from fastapi.responses import FileResponse

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["uploads"])


@router.post("/uploads")
async def upload_track(
    file: UploadFile,
    user: User = Depends(get_current_user),
) -> dict:
    from app.services.upload_service import UploadService

    service = UploadService()
    track = await service.process(file=file, user_id=user.id)
    return {"track": track}


@router.get("/uploads")
async def list_uploads(
    q: str | None = Query(None, max_length=200),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
) -> dict:
    from app.services.upload_service import UploadService

    service = UploadService()
    tracks = await service.list_tracks(query=q, limit=limit, offset=offset)
    return {"tracks": tracks}


@router.get("/uploads/{track_id}")
async def get_upload(track_id: str, user: User = Depends(get_current_user)) -> dict:
    from app.services.upload_service import UploadService

    service = UploadService()
    track = await service.get_track(track_id)
    return {"track": track}


@router.get("/uploads/{track_id}/file")
async def get_upload_file(track_id: str, user: User = Depends(get_current_user)) -> FileResponse:
    from app.services.upload_service import UploadService

    service = UploadService()
    file_path = await service.get_file_path(track_id)
    return FileResponse(file_path, media_type="audio/mpeg")
