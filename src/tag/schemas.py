from pydantic import BaseModel
from datetime import datetime


class TagSchemaRequest(BaseModel):
    name: str
    description: str


class TagSchemaUpdateRequest(TagSchemaRequest):
    pass


class TagSchemaResponse(TagSchemaRequest):
    id: int

    class Config:
        from_attributes: True


