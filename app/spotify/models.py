from pydantic import BaseModel, Field, field_validator
from app.config import settings


class Base(BaseModel):
    class Config:
        extra = "ignore"


class TrackModel(Base):
    id: str
    name: str
    artists: str

    @field_validator("artists", mode="before")
    def validate_artists(cls, value: list[dict] | str):
        if isinstance(value, list):
            return ", ".join(artist["name"] for artist in value)
        return value


class AuthModel(Base):
    access_token: str
    refresh_token: str
    expires_in: int = Field(default=3600, ge=0)


class RefreshTokenAuthModel(Base):
    access_token: str 
    token_type: str = "Bearer"
    expires_in: int = Field(default=3600, ge=0)
    scope: str = settings.spotify_scope


class AuthorizeRequestModel(Base):
    response_type: str = "code"
    client_id: str = settings.spotify_client_id
    scope: str = settings.spotify_scope
    redirect_uri: str = settings.spotify_redirect_uri

    @property
    def url(self) -> str:
        query = "&".join([f"{k}={v}" for k, v in self.model_dump().items()])
        return f"https://accounts.spotify.com/authorize?{query}"
