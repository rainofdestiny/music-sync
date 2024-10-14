from pydantic import BaseModel, Field, validator
from app.config import settings


class Base(BaseModel):
    class Config:
        extra = "ignore"


class TrackModel(Base):
    id: str
    name: str
    artists: str  # Список артистов

    @validator("artists", pre=True, always=True)
    def validate_artists(cls, value):
        if isinstance(value, list):
            return ", ".join(artist["name"] for artist in value)
        return value


class AuthModel(Base):
    access_token: str
    refresh_token: str
    expires_in: int = Field(default=3600, ge=0)


class AuthorizeRequestModel(Base):
    response_type: str = "code"
    client_id: str = settings.spotify_client_id
    scope: str = "user-read-currently-playing user-library-read"
    redirect_uri: str = settings.spotify_redirect_uri

    @property
    def query(self) -> str:
        return "&".join([f"{k}={v}" for k, v in self.dict().items()])

    @property
    def url(self) -> str:
        return f"https://accounts.spotify.com/authorize?{self.query}"
