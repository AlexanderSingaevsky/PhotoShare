import typing
import uuid
from pydantic import BaseModel, Field
from datetime import datetime


class ImageSchemaRequest(BaseModel):
    title: str = Field()


class ImageSchemaUpdateRequest(ImageSchemaRequest):
    title: str = Field(default=None)


T = typing.TypeVar("T")


class BaseTransformation(BaseModel, typing.Generic[T]):
    pass


class ImageAIReplaceTransformation(BaseTransformation):
    Object_to_detect: str = Field(default="")
    Replace_with: str = Field(default="")

    class Config:
        from_attributes: True


class ImageScaleTransformation(BaseTransformation):
    Width: int = Field(default=500)
    Height: int = Field(default=500)

    class Config:
        from_attributes: True


class ImageBlackAndWhiteTransformation(BaseTransformation):
    black_and_white: bool = Field(default=False)

    class Config:
        from_attributes: True


class ImageRotationTransformation(BaseTransformation):
    angle: int = Field(default=0, le=360, ge=-360)

    class Config:
        from_attributes: True


class ImageFlipModeTransformation(BaseTransformation):
    flip_mode: str = Field(
        default="ignore",
        examples=["vflip", "hflip", "ignore", "auto_right", "auto_left"],
    )

    class Config:
        from_attributes: True


class EditFormData(BaseTransformation):
    ai_replace: ImageAIReplaceTransformation
    scale: ImageScaleTransformation
    black_and_white: ImageBlackAndWhiteTransformation
    rotation: ImageRotationTransformation
    flip_mode: ImageFlipModeTransformation


class ImageSchemaResponse(ImageSchemaRequest):
    id: int
    owner_id: uuid.UUID
    cloudinary_url: str
    edited_cloudinary_url: str = Field(default="")
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes: True
