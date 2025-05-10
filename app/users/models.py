from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.types import created_at, intpk, updated_at

__all__ = ["UsersOrm"]


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    active_async: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at | None]

    def __repr__(self) -> str:
        return f"<UsersOrm(id={self.id} username='{self.username}')>"
