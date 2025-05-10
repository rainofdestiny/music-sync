from sqlalchemy import String, relationship, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.types import created_at, intpk, updated_at

__all__ = ["SpotifyOrm"]


class SpotifyOrm(Base):
    __tablename__ = "spotify"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]

    users: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="spotify")
