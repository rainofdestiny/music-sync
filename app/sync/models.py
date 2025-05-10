from sqlalchemy import String, relationship, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.types import created_at, intpk

__all__ = ["SyncedTracksOrm"]


class SyncedTracksOrm(Base):
    __tablename__ = "synced_tracks"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    spotify_track_id: Mapped[str] = mapped_column(String(255), nullable=True)
    yandex_track_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[created_at]

    users: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="synced_tracks")
