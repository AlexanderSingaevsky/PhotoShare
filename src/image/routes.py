from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio.client import Redis

from src.database.sql.postgres_conn import database
from src.database.cache.redis_conn import cache_database

router = APIRouter(prefix='/image', tags=["images"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_contact(user=None,
                         db: AsyncSession = Depends(database),
                         cache: Redis = Depends(cache_database)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/{image_id}")
async def get_image(image_id: str,
                    user=None,
                    db: AsyncSession = Depends(database),
                    cache: Redis = Depends(cache_database)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.get("/search/{image_search_string}")
async def search_image(image_search_string: str,
                       user=None,
                       db: AsyncSession = Depends(database),
                       cache: Redis = Depends(cache_database)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.put("/update/{image_id}")
async def update_image(image_id: str,
                       user=None,
                       db: AsyncSession = Depends(database),
                       cache: Redis = Depends(cache_database)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)


@router.delete("/delete/{image_id}")
async def delete_image(image_id: str,
                       user=None,
                       db: AsyncSession = Depends(database),
                       cache: Redis = Depends(cache_database)):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
