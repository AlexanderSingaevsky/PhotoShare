import uuid
from pydantic import BaseModel, Field
from datetime import datetime


class ImageSchemaRequest(BaseModel):
    title: str = Field()


class ImageSchemaUpdateRequest(ImageSchemaRequest):
    pass


class ImageSchemaOnEditRequest(BaseModel):
    ai_replace: dict = Field(
        description="AI replace",
        example={"Object to detect": "apple", "Replace with": "orange"},
        default=None,  # Додаємо default=None, щоб поле було необов'язковим
    )
    scale: dict = Field(
        description="Scale",
        example={"Width": 500, "Height": 500},
        default=None,  # Додаємо default=None, щоб поле було необов'язковим
    )
    black_and_white: bool = Field(
        description="Black and white",
        default=None,
    )
    rotation: int = Field(description="Rotation", default=None, le=360, ge=-360)
    flip_mode: dict = Field(
        description="""
        Flip mode. Possible values:
        vflip: Vertically mirror flips the image.
        hflip: Horizontally mirror flips the image.
        ignore: By default, the image is automatically rotated according to the EXIF data stored by the camera when the image was taken. Set the rotation to ignore if you do not want the image to be automatically rotated.
        auto_right: If the requested aspect ratio of a crop does not match the image's original aspect ratio (landscape vs portrait ratio), rotates the image 90 degrees clockwise. Must be used as a qualifier of a cropping action.
        auto_left: If the requested aspect ratio of a crop does not match the image's original aspect ratio (it is greater than 1, while the original is less than 1, or vice versa), rotates the image 90 degrees counterclockwise. Must be used as a qualifier of a cropping action.""",
        default=None,
        example={"flip_mode": "vflip"},
    )


class ImageSchemaResponse(ImageSchemaRequest):
    id: int
    owner_id: uuid.UUID
    cloudinary_url: str
    edited_cloudinary_url: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes: True
