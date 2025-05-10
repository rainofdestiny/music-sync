from typing import Any

from pydantic import Field, field_validator

from app.config import settings
from app.schemas import Base


class TrackSchema(Base):
    id: str
    name: str
    artists: str

    @field_validator("artists", mode="before")
    def validate_artists(cls, value: list[dict[str, Any]] | str) -> str:
        if isinstance(value, list):
            return ", ".join([artist["name"] for artist in value])
        return value


class AuthSchema(Base):
    access_token: str
    refresh_token: str
    expires_in: int = Field(default=3600, ge=0)


class RefreshTokenAuthSchema(Base):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = Field(default=3600, ge=0)
    scope: str = Field(default=settings.spotify_scope)


class UserProfileSchema(Base):
    id: str
    display_name: str
    email: str
    uri: str
    country: str
