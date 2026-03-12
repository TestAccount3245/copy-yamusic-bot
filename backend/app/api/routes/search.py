from fastapi import APIRouter, Depends, Query

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["search"])


@router.get("/search")
async def search(
    q: str = Query(..., min_length=1, max_length=200),
    type: str = Query("track", pattern="^(track|album|artist|all)$"),
    user: User = Depends(get_current_user),
) -> dict:
    from app.services.search_service import SearchService

    service = SearchService()
    results = await service.search(query=q, search_type=type, user=user)
    return {"results": results}
