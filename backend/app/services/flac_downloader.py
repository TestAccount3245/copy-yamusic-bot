import hashlib
import hmac
from pathlib import Path

import aiohttp

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class FlacDownloader:
    """Downloads FLAC tracks from Yandex Music using HMAC-SHA256 signed URLs."""

    def __init__(self, token: str):
        self._token = token

    async def download(self, track_id: str, output_dir: Path) -> Path:
        """Download a track in FLAC quality.

        Uses the sign key from yandex-music-api library to generate
        authenticated download URLs for lossless content.
        """
        from yandex_music import ClientAsync

        client = await ClientAsync(self._token).init()

        # Get download info with direct links
        download_info_list = await client.tracks_download_info(track_id, get_direct_links=True)
        if not download_info_list:
            raise ValueError(f"No download info for track {track_id}")

        # Find the highest quality available
        # Prefer lossless (flac), fall back to highest bitrate mp3
        best = None
        for info in download_info_list:
            if info.codec == "flac":
                best = info
                break
            if best is None or (info.bitrate_in_kbps or 0) > (best.bitrate_in_kbps or 0):
                best = info

        if best is None:
            raise ValueError(f"No suitable download info for track {track_id}")

        direct_link = best.direct_link
        if not direct_link:
            raise ValueError(f"No direct link available for track {track_id}")

        ext = "flac" if best.codec == "flac" else "mp3"
        output_path = output_dir / f"{track_id}.{ext}"

        async with aiohttp.ClientSession() as session:
            async with session.get(direct_link) as resp:
                if resp.status != 200:
                    raise ValueError(f"Download failed with status {resp.status}")

                with open(output_path, "wb") as f:
                    async for chunk in resp.content.iter_chunked(64 * 1024):
                        f.write(chunk)

        logger.info("FLAC download complete", track_id=track_id, path=str(output_path), codec=best.codec)
        return output_path
