from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.postgres_conn import database
from src.database.cache.redis_conn import cache_database
from src.image.schemas import ImageCreate, ImageUpdate, Image
from src.image.repository import ImageRepository

router = APIRouter(prefix='/images', tags=["images"])

@router.post("/upload", response_model=Image, status_code=status.HTTP_201_CREATED)
async def upload_image(image: ImageCreate, db: AsyncSession = Depends(database)):
    image_repo = ImageRepository(db)
    db_image = await image_repo.create_image(image.dict())
    return db_image


@router.get("/{image_id}", response_model=Image)
async def get_image(image_id: int, db: AsyncSession = Depends(database)):
    image_repo = ImageRepository(db)
    db_image = await image_repo.get_image(image_id)
    if db_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return db_image


@router.put("/{image_id}", response_model=Image)
async def update_image(image_id: int, image_update: ImageUpdate, db: AsyncSession = Depends(database)):
    image_repo = ImageRepository(db)
    db_image = await image_repo.get_image(image_id)
    if db_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    updated_image = await image_repo.update_image(db_image, image_update.dict())
    return updated_image


@router.delete("/{image_id}", response_model=dict)
async def delete_image(image_id: int, db: AsyncSession = Depends(database)):
    image_repo = ImageRepository(db)
    db_image = await image_repo.get_image(image_id)
    if db_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    await image_repo.delete_image(db_image)
    return {"message": "Image deleted"}


@router.get("/search/{image_search_string}", response_model=list[Image])
async def search_images(image_search_string: str, db: AsyncSession = Depends(database)):
    image_repo = ImageRepository(db)
    images = await image_repo.search_images(image_search_string)
    return images
