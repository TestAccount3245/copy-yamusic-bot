from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["users"])


class LinkYandexRequest(BaseModel):
    token: str


class UpdateSettingsRequest(BaseModel):
    preferred_quality: str | None = None


@router.get("/users/me")
async def get_me(user: User = Depends(get_current_user)) -> dict:
    return {
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "preferred_quality": user.preferred_quality,
            "has_yandex": user.yandex_token is not None,
        }
    }


@router.post("/users/link-yandex")
async def link_yandex(
    body: LinkYandexRequest,
    user: User = Depends(get_current_user),
) -> dict:
    from app.services.user_service import UserService

    service = UserService()
    await service.link_yandex_token(user_id=user.id, token=body.token)
    return {"status": "linked"}


@router.put("/users/settings")
async def update_settings(
    body: UpdateSettingsRequest,
    user: User = Depends(get_current_user),
) -> dict:
    from app.services.user_service import UserService

    service = UserService()
    await service.update_settings(user_id=user.id, **body.model_dump(exclude_none=True))
    return {"status": "updated"}
