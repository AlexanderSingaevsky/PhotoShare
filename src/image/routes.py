from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis

from src.database.sql.alchemy_models import User
from src.auth.service import current_active_user
from src.database.sql.postgres_conn import database
from src.database.cache.redis_conn import cache_database
from src.image.repository import ImageQuery
from src.image.schemas import (
    ImageSchemaRequest,
    ImageSchemaResponse,
    ImageSchemaUpdateRequest,
    ImageSchemaOnEditRequest,
)
from src.auth.utils.access import access_service
from src.image.utils.cloudinary_service import UploadImage

router = APIRouter(prefix="/image", tags=["images"])


@router.post(
    "/create", response_model=ImageSchemaResponse, status_code=status.HTTP_201_CREATED
)
async def create_image(
    title: str = Form(),
    image_file: UploadFile = File(),
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(database),
    cache: Redis = Depends(cache_database),
):
    # access_service('can_add_image', user)  # TODO
    public_id = UploadImage.generate_name_folder(user)
    r = UploadImage.upload(image_file.file, public_id)
    src_url = UploadImage.get_pic_url(public_id, r)
    image = await ImageQuery.create(title, src_url, user, db)
    return image


@router.get("/{image_id}", response_model=ImageSchemaResponse)
async def get_image(
    image_id: int,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(database),
    cache: Redis = Depends(cache_database),
):
    # access_service('can_add_image', user)  # TODO
    image = await ImageQuery.read(image_id, db)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found!"
        )
    return image


@router.post("/edit/{image_id}", response_model=ImageSchemaResponse)
async def edit_image(
    image_id: int,
    edit_data: ImageSchemaOnEditRequest,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(database),
    cache: Redis = Depends(cache_database),
    # image_data: ImageSchemaUpdateRequest = None,
):
    image = await get_image(image_id, user, db, cache)
    original_img_url = image.cloudinary_url
    edited_img_url = UploadImage.edit_image(original_img_url, edit_data)
    image = await ImageQuery.add_edited_url(image_id, db, edited_img_url)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found!"
        )
    return image


@router.get("/search/{image_search_string}")
async def search_image(
    image_search_string: str,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(database),
    cache: Redis = Depends(cache_database),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.put("/update/{image_id}", response_model=ImageSchemaResponse)
async def update_image(
    image_id: int,
    image_data: ImageSchemaUpdateRequest,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(database),
    cache: Redis = Depends(cache_database),
):
    access_service("can_add_image", user)  # TODO
    image = await ImageQuery.update(image_id, image_data, db)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found!"
        )
    return image


@router.delete("/delete/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(
    image_id: int,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(database),
    cache: Redis = Depends(cache_database),
):
    access_service("can_add_image", user)  # TODO
    await ImageQuery.delete(image_id, db)
