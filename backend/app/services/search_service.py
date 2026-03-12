from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.uploaded_track import UploadedTrack
from app.models.user import User
from app.services.yandex_music import YandexMusicService


class SearchService:
    async def search(
        self,
        query: str,
        search_type: str,
        user: User,
        session: AsyncSession | None = None,
    ) -> dict:
        results: dict = {"tracks": [], "albums": [], "artists": []}

        # Search Yandex Music (if user has token)
        if user.yandex_token:
            ym = YandexMusicService(user.yandex_token)
            ym_results = await ym.search(query, search_type)
            results["tracks"].extend(ym_results.get("tracks", []))
            results["albums"].extend(ym_results.get("albums", []))
            results["artists"].extend(ym_results.get("artists", []))

        # Search uploaded tracks (always)
        if session and search_type in ("track", "all"):
            uploaded = await self._search_uploaded(query, session)
            results["tracks"].extend(uploaded)

        return results

    @staticmethod
    async def _search_uploaded(query: str, session: AsyncSession) -> list[dict]:
        stmt = (
            select(UploadedTrack)
            .where(
                UploadedTrack.search_vector.op("@@")(
                    text("plainto_tsquery('russian', :q)")
                )
            )
            .params(q=query)
            .limit(20)
        )
        result = await session.execute(stmt)
        tracks = result.scalars().all()

        return [
            {
                "id": f"upload:{t.id}",
                "title": t.title,
                "artist": t.artist or "Unknown",
                "album": t.album,
                "duration_sec": t.duration_sec,
                "source": "uploaded",
            }
            for t in tracks
        ]
