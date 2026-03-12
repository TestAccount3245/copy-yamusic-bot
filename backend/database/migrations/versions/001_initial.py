"""Initial tables: users, uploaded_tracks, download_logs

Revision ID: 001
Revises:
Create Date: 2026-03-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("username", sa.String(64)),
        sa.Column("first_name", sa.String(128)),
        sa.Column("yandex_token", sa.String(512)),
        sa.Column("preferred_quality", sa.String(8), server_default="mp3"),
        sa.Column("api_key", sa.String(64), unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "uploaded_tracks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("uploader_id", sa.BigInteger(), sa.ForeignKey("users.id")),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("artist", sa.String(256)),
        sa.Column("album", sa.String(256)),
        sa.Column("duration_sec", sa.Integer()),
        sa.Column("bitrate_kbps", sa.Integer()),
        sa.Column("format", sa.String(8)),
        sa.Column("file_size_bytes", sa.BigInteger()),
        sa.Column("file_path", sa.String(512), nullable=False),
        sa.Column("search_vector", TSVECTOR()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_uploads_search", "uploaded_tracks", ["search_vector"], postgresql_using="gin")

    op.create_table(
        "download_logs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id")),
        sa.Column("track_source", sa.String(16), nullable=False),
        sa.Column("track_id", sa.String(64), nullable=False),
        sa.Column("quality", sa.String(8)),
        sa.Column("file_size_bytes", sa.BigInteger()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("idx_dl_user_time", "download_logs", ["user_id", "created_at"])


def downgrade() -> None:
    op.drop_table("download_logs")
    op.drop_table("uploaded_tracks")
    op.drop_table("users")
