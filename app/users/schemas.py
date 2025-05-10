from datetime import datetime

from pydantic import Field

from app.schemas import Base


class UserBaseSchema(Base):
    username: str


class UserCreateSchema(Base):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)


class UserLoginSchema(Base):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)


class UserReadSchema(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
