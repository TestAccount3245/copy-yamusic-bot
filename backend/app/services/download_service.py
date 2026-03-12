import zipfile
from pathlib import Path

import aiohttp

from app.core.config import settings
from app.core.logging import get_logger
from app.models.user import User
from app.services.cache_service import CacheService
from app.services.flac_downloader import FlacDownloader
from app.services.yandex_music import YandexMusicService

logger = get_logger(__name__)


class DownloadService:
    def __init__(self):
        self._cache = CacheService()
        self._cache_dir = Path(settings.storage_path) / "cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    async def download_track(self, track_id: str, quality: str, user: User) -> dict:
        """Download a single track. Returns file path and metadata."""
        cached = await self._cache.get(track_id, quality)
        if cached and Path(cached).exists():
            logger.info("Cache hit", track_id=track_id, quality=quality)
            return {"file_path": cached, "file_size": Path(cached).stat().st_size}

        ym = YandexMusicService(user.yandex_token)
        track_info = await ym.get_track(track_id)

        if quality == "flac":
            downloader = FlacDownloader(user.yandex_token)
            file_path = await downloader.download(track_id, self._cache_dir)
        else:
            file_path = await self._download_mp3(ym, track_id)

        await self._cache.set(track_id, quality, str(file_path))

        return {
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "title": track_info.get("title", "Unknown"),
            "artist": track_info.get("artist", "Unknown"),
        }

    async def download_album(self, album_id: str, quality: str, user: User) -> dict:
        """Download all tracks in an album as a zip."""
        ym = YandexMusicService(user.yandex_token)
        album = await ym.get_album(album_id)

        tracks = album.get("tracks", [])
        files = []

        for track in tracks:
            result = await self.download_track(track["id"], quality, user)
            files.append((result["file_path"], f"{track['artist']} - {track['title']}"))

        zip_path = self._cache_dir / f"album_{album_id}.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for file_path, name in files:
                ext = Path(file_path).suffix
                zf.write(file_path, f"{name}{ext}")

        return {
            "file_path": str(zip_path),
            "tracks_count": len(files),
            "album_title": album.get("title", "Unknown"),
            "artist": album.get("artist", "Unknown"),
        }

    async def download_artist(self, artist_id: str, user: User) -> dict:
        """Download artist's top tracks."""
        ym = YandexMusicService(user.yandex_token)
        artist = await ym.get_artist(artist_id)

        quality = user.preferred_quality or "mp3"
        files = []

        for track in artist.get("top_tracks", []):
            result = await self.download_track(track["id"], quality, user)
            files.append((result["file_path"], f"{track['artist']} - {track['title']}"))

        zip_path = self._cache_dir / f"artist_{artist_id}.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            for file_path, name in files:
                ext = Path(file_path).suffix
                zf.write(file_path, f"{name}{ext}")

        return {
            "file_path": str(zip_path),
            "tracks_count": len(files),
            "artist_name": artist.get("name", "Unknown"),
        }

    async def _download_mp3(self, ym: YandexMusicService, track_id: str) -> Path:
        """Download track in mp3 using the standard API."""
        download_info = await ym.get_download_info(track_id)
        if not download_info:
            raise ValueError(f"No download info for track {track_id}")

        # Pick highest bitrate mp3
        best = max(
            (d for d in download_info if d.codec == "mp3"),
            key=lambda d: d.bitrate_in_kbps or 0,
            default=download_info[0],
        )

        direct_link = best.direct_link
        if not direct_link:
            raise ValueError(f"No direct link for track {track_id}")

        output_path = self._cache_dir / f"{track_id}.mp3"

        async with aiohttp.ClientSession() as session:
            async with session.get(direct_link) as resp:
                if resp.status != 200:
                    raise ValueError(f"Download failed: HTTP {resp.status}")
                with open(output_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(64 * 1024):
                        f.write(chunk)

        logger.info("MP3 download complete", track_id=track_id, path=str(output_path))
        return output_path
