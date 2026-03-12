import uuid
from pathlib import Path

import aiofiles
import magic
from fastapi import UploadFile
from mutagen import File as MutagenFile

from app.core.config import settings
from app.core.exceptions import ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)

ALLOWED_MIME_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/flac",
    "audio/ogg",
    "audio/wav",
    "audio/x-wav",
    "audio/x-flac",
}

ALLOWED_EXTENSIONS = {".mp3", ".flac", ".ogg", ".wav"}


class UploadService:
    def __init__(self):
        self._upload_dir = Path(settings.storage_path) / "uploads"
        self._upload_dir.mkdir(parents=True, exist_ok=True)

    async def process(self, file: UploadFile, user_id: int) -> dict:
        """Validate, save, and index an uploaded track."""
        # Validate extension
        if not file.filename:
            raise ValidationError("Filename required")

        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError(f"Unsupported format. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

        # Read file content
        content = await file.read()

        # Validate size
        if len(content) > settings.upload_max_size_bytes:
            raise ValidationError(f"File too large. Max: {settings.upload_max_size_mb}MB")

        # Validate MIME type using magic bytes
        mime = magic.from_buffer(content[:2048], mime=True)
        if mime not in ALLOWED_MIME_TYPES:
            raise ValidationError(f"Invalid audio file. Detected MIME: {mime}")

        # Save file
        file_id = uuid.uuid4()
        file_path = self._upload_dir / f"{file_id}{ext}"
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        # Extract metadata
        metadata = self._extract_metadata(file_path)

        logger.info("Track uploaded", file_id=str(file_id), user_id=user_id, **metadata)

        # TODO: insert into DB (uploaded_tracks table) with tsvector

        return {
            "id": str(file_id),
            "file_path": str(file_path),
            "file_size_bytes": len(content),
            "format": ext.lstrip("."),
            **metadata,
        }

    @staticmethod
    def _extract_metadata(file_path: Path) -> dict:
        """Extract audio metadata using mutagen."""
        try:
            audio = MutagenFile(str(file_path))
            if audio is None:
                return {"title": file_path.stem, "artist": None, "album": None, "duration_sec": None, "bitrate_kbps": None}

            title = None
            artist = None
            album = None

            if hasattr(audio, "tags") and audio.tags:
                tags = audio.tags
                # Handle different tag formats
                title = str(tags.get("TIT2", tags.get("title", [None]))[0]) if tags.get("TIT2") or tags.get("title") else None
                artist = str(tags.get("TPE1", tags.get("artist", [None]))[0]) if tags.get("TPE1") or tags.get("artist") else None
                album = str(tags.get("TALB", tags.get("album", [None]))[0]) if tags.get("TALB") or tags.get("album") else None

            duration_sec = int(audio.info.length) if hasattr(audio, "info") and audio.info else None
            bitrate_kbps = int(audio.info.bitrate / 1000) if hasattr(audio, "info") and hasattr(audio.info, "bitrate") and audio.info.bitrate else None

            return {
                "title": title or file_path.stem,
                "artist": artist,
                "album": album,
                "duration_sec": duration_sec,
                "bitrate_kbps": bitrate_kbps,
            }
        except Exception as e:
            logger.warning("Metadata extraction failed", error=str(e))
            return {"title": file_path.stem, "artist": None, "album": None, "duration_sec": None, "bitrate_kbps": None}

    async def get_track(self, track_id: str) -> dict:
        # TODO: fetch from DB
        raise NotImplementedError

    async def list_tracks(self, query: str | None, limit: int, offset: int) -> list[dict]:
        # TODO: fetch from DB with optional search
        raise NotImplementedError

    async def get_file_path(self, track_id: str) -> str:
        # TODO: fetch file_path from DB
        raise NotImplementedError
