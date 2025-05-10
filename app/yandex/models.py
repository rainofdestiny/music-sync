from sqlalchemy import Boolean, String, relationship, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.types import created_at, intpk, updated_at

__all__ = ["SpotifyLastLikedTrackOrm"]


class YandexOrm(Base):
    __tablename__ = "yandex"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]

    users: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="yandex")
