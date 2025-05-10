import re

from pydantic import field_validator

from app.schemas import Base


class ArtistSchema(Base):
    id: int
    name: str


class TrackSchema(Base):
    id: int
    title: str
    artists: list[ArtistSchema]

    @property
    def full_title(self):
        artists = ", ".join([artist.name for artist in self.artists])
        return f"{artists} - {self.title}"

    @field_validator("title", mode="before")
    def remove_parentheses(cls, value: str) -> str:
        return re.sub(r"\s*\(.*?\)", "", value).strip()
