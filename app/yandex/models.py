from pydantic import BaseModel, Field


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


class TrackIdsModel(Base):
    spotify: str = Field(alias="s")
    yandex: int = Field(alias="y")
