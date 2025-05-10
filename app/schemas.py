from pydantic import (  # type: ignore (Pyright: Type of "Field" is partially unknown)
    BaseModel,
    ConfigDict,
    Field,
)


class Base(BaseModel):
    model_config = ConfigDict(extra="ignore", from_attributes=True)


class PaginationSchema(BaseModel):
    limit: int = Field(50, ge=1)
    offset: int = Field(0, ge=0)
