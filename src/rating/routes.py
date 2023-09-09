from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import current_active_user
from src.database.sql.alchemy_models import User
from src.database.sql.postgres_conn import database
from src.rating.repository import RatingQuery
from src.rating.schemas import RatingSchemaResponse, RatingSchemaRequest, RatingUpdateSchemaRequest

router = APIRouter(prefix="/rating", tags=["ratings"])


@router.post('/create', name="Add new rating", response_model=RatingSchemaResponse, status_code=status.HTTP_201_CREATED)
async def create_rating(body: RatingSchemaRequest,
                        user: User = Depends(current_active_user),
                        db: AsyncSession = Depends(database)):
    rating = await RatingQuery.create(body, user, db)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found!')
    return rating


@router.put('/update/{rating_id}', response_model=RatingSchemaResponse)
async def update_rating(rating_id: int,
                        body: RatingUpdateSchemaRequest,
                        user: User = Depends(current_active_user),
                        db: AsyncSession = Depends(database)):
    rating = await RatingQuery.update(rating_id, body, db)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Rating not found!')
    return rating
