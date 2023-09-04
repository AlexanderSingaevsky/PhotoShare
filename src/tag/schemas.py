from pydantic import BaseModel
from datetime import datetime


class TagCreate(BaseModel):
    name: str


class TagUpdate(BaseModel):
    name: str


class Tag(TagCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None
