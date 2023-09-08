from typing import Union, Type, Literal

from fastapi import APIRouter, HTTPException, status, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import current_active_user
from src.database.cache.redis_conn import cache_database
from src.database.sql.alchemy_models import User
from src.database.sql.postgres_conn import database
from src.image.routes import get_image
from src.image.schemas import (
    ImageScaleTransformation,
    ImageAIReplaceTransformation,
    ImageBlackAndWhiteTransformation,
    ImageRotationTransformation,
    ImageFlipModeTransformation,
)
from src.image.utils.cloudinary_service import ImageEditor

transformation_router = APIRouter(prefix="/image_transform", tags=["images"])


@transformation_router.get(
    "/get_transformation_form/{transformation_type}",
)
async def get_transformation_form(
    transformation_type: Literal[
        "ai_replace", "scale", "black_and_white", "rotation", "flip_mode"
    ],
    user: User = Depends(current_active_user),
):
    """
    Приймає тип трансформації і відображає форму для редагування
    Можливі типи трансформацій:
    ai_replace, scale, black_and_white, rotation, flip_mode
    """
    transformation_types = {
        "scale": ImageScaleTransformation,
        "ai_replace": ImageAIReplaceTransformation,
        "black_and_white": ImageBlackAndWhiteTransformation,
        "rotation": ImageRotationTransformation,
        "flip_mode": ImageFlipModeTransformation,
    }
    if transformation_type not in transformation_types.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transformation type does not exist!",
        )
    model = transformation_types.get(transformation_type)[0]()
    response = {f"{transformation_type}": model.model_dump()}
    print(response)
    return response

    # return transformation_types.


def create_transformation_route(
    transformation_type: str,
    transformation: Type[
        Union[
            ImageAIReplaceTransformation,
            ImageScaleTransformation,
            ImageBlackAndWhiteTransformation,
            ImageRotationTransformation,
            ImageFlipModeTransformation,
        ]
    ],
):
    async def route(
        image_id: int,
        transformation_data: transformation,
        user: User = Depends(current_active_user),
        db: AsyncSession = Depends(database),
        cache: Redis = Depends(cache_database),
    ):
        image = await get_image(image_id, user, db, cache)
        original_img_url = image.cloudinary_url
        edited_img_url = await ImageEditor().edit_image(
            original_img_url, transformation_data
        )
        return edited_img_url

    route.__name__ = transformation_type
    return route


transformation_router.add_api_route(
    "/ai_replace/{image_id}",
    create_transformation_route("ai_replace", ImageAIReplaceTransformation),
    methods=["POST"],
)

transformation_router.add_api_route(
    "/scale/{image_id}",
    create_transformation_route("scale", ImageScaleTransformation),
    methods=["POST"],
)

transformation_router.add_api_route(
    "/black_and_white/{image_id}",
    create_transformation_route("black_and_white", ImageBlackAndWhiteTransformation),
    methods=["POST"],
)

transformation_router.add_api_route(
    "/rotation/{image_id}",
    create_transformation_route("rotation", ImageRotationTransformation),
    methods=["POST"],
)

transformation_router.add_api_route(
    "/flip_mode/{image_id}",
    create_transformation_route("flip_mode", ImageFlipModeTransformation),
    methods=["POST"],
    description="""
        Flip mode. Possible values:
        vflip: Vertically mirror flips the image.
        hflip: Horizontally mirror flips the image.
        ignore: By default, the image is automatically rotated according to the EXIF data stored by the camera when the image was taken. Set the rotation to ignore if you do not want the image to be automatically rotated.
        auto_right: If the requested aspect ratio of a crop does not match the image's original aspect ratio (landscape vs portrait ratio), rotates the image 90 degrees clockwise. Must be used as a qualifier of a cropping action.
        auto_left: If the requested aspect ratio of a crop does not match the image's original aspect ratio (it is greater than 1, while the original is less than 1, or vice versa), rotates the image 90 degrees counterclockwise. Must be used as a qualifier of a cropping action.""",
)
