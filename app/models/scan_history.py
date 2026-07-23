"""
ScanHistory ORM model.

Persists every message analysis result from the AI detection pipeline.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.database.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class ScanHistory(Base):
    """A single scam-detection scan and its AI-generated result."""

    __tablename__ = "scan_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Optional link to authenticated user; null for anonymous scans
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    message: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(50), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    # Stored as JSON arrays in SQLite
    keywords: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    urls: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    reason: Mapped[str] = mapped_column(Text, nullable=False)
    advice: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )

    user: Mapped["User | None"] = relationship(back_populates="scan_histories")

    def __repr__(self) -> str:
        return f"<ScanHistory id={self.id} status={self.status!r} risk_score={self.risk_score}>"
