import re
from pydantic import BaseModel, Field, field_validator


class Base(BaseModel):
    class Config:
        extra = "ignore"


class TrackModel(Base):
    id: str
    name: str
    artists: str

    @property
    def full_title(self):
        return f"{self.artists} - {self.name}"

    @field_validator("name", mode="before")
    def remove_parentheses(cls, value: str) -> str:
        return re.sub(r"\s*\(.*?\)", "", value).strip()


class TrackIdsModel(Base):
    spotify: str = Field(alias="s")
    yandex: int = Field(alias="y")
