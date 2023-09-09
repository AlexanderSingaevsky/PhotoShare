from fastapi import APIRouter, Depends, status, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import current_active_user
from src.database.sql.alchemy_models import User
from src.database.sql.postgres_conn import database
from src.image.repository import ImageQuery
from src.rating.repository import RatingQuery
from src.rating.schemas import RatingSchemaResponse, RatingSchemaRequest, RatingUpdateSchemaRequest

router = APIRouter(prefix="/rating", tags=["ratings"])


@router.get('/{rating_id}', response_model=RatingSchemaResponse, name="Get one rating")
async def get_rating(rating_id: int = Path(ge=1), user: User = Depends(current_active_user),
                      db: AsyncSession = Depends(database)):
    rating = await RatingQuery.read(rating_id, db)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Rating not found!')
    return rating


@router.post('/create', name="Add new rating", response_model=RatingSchemaResponse, status_code=status.HTTP_201_CREATED)
async def create_rating(body: RatingSchemaRequest,
                        user: User = Depends(current_active_user),
                        db: AsyncSession = Depends(database)):
    image = await ImageQuery.read(body.image_id, db)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image does not exist!')
    rating = await RatingQuery.create(body, user, image, db)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found!')
    return rating


@router.put('/update/{rating_id}', response_model=RatingSchemaResponse, name='Update rating')
async def update_rating(rating_id: int,
                        body: RatingUpdateSchemaRequest,
                        user: User = Depends(current_active_user),
                        db: AsyncSession = Depends(database)):
    rating = await RatingQuery.read(rating_id, db)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Rating not found!')
    return await RatingQuery.update(rating_id, body, user, db)


@router.delete('/delete/{rating_id}', status_code=status.HTTP_204_NO_CONTENT, name='Delete rating')
async def delete_rating(rating_id: int,
                        user: User = Depends(current_active_user),
                        db: AsyncSession = Depends(database)):
    rating = await RatingQuery.read(rating_id, db)
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Rating not found!')
    await RatingQuery.delete(rating_id, user, db)
