import uuid
from pydantic import BaseModel, Field
from datetime import datetime


class ImageSchemaRequest(BaseModel):
    title: str = Field()


class ImageSchemaUpdateRequest(ImageSchemaRequest):
    pass


class ImageSchemaResponse(ImageSchemaRequest):
    id: int
    owner_id: uuid.UUID
    cloudinary_url: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes: True
