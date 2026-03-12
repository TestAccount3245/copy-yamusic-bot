import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class UploadedTrack(Base):
    __tablename__ = "uploaded_tracks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uploader_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    artist: Mapped[str | None] = mapped_column(String(256))
    album: Mapped[str | None] = mapped_column(String(256))
    duration_sec: Mapped[int | None] = mapped_column(Integer)
    bitrate_kbps: Mapped[int | None] = mapped_column(Integer)
    format: Mapped[str | None] = mapped_column(String(8))
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_uploads_search", "search_vector", postgresql_using="gin"),
    )
