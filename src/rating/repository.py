from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql.alchemy_models import User, Rating, Image
from src.image.repository import ImageQuery


class RatingQuery:
    @classmethod
    async def _update_average_rating(cls, image: Image, db: AsyncSession):
        ratings = await db.execute(select(Rating).filter(Rating.image_id == image.id))
        ratings = ratings.scalars().all()
        total_rating = sum(rating.value for rating in ratings)
        average_rating = total_rating / len(ratings) if ratings else 0
        image.rating = average_rating
        await db.commit()

    @staticmethod
    async def read(rating_id: int, db: AsyncSession) -> Rating | None:
        sq = select(Rating).filter_by(id=rating_id)
        rating = await db.execute(sq)
        rating = rating.scalar_one_or_none()
        return rating

    @staticmethod
    async def create(body, user: User, image: Image, db: AsyncSession) -> Rating:
        rating = await db.scalar(
            select(Rating).where(
                (Rating.owner_id == user.id) & (Rating.image_id == image.id)
            )
        )
        if rating:
            rating.value = body.value
        else:
            rating = Rating(**body.model_dump(), owner_id=user.id)
        db.add(rating)
        await db.commit()
        await db.refresh(rating)
        await RatingQuery._update_average_rating(image, db)
        return rating

    @staticmethod
    async def update(rating_id: int, body, user, db) -> Rating | None:
        rating = await db.scalar(
            select(Rating).where(
                (Rating.owner_id == user.id) & (Rating.id == rating_id)
            )
        )
        if not rating:
            return None
        rating.value = body.value
        await db.commit()
        await db.refresh(rating)
        image = await db.get(Image, rating.image_id)
        await RatingQuery._update_average_rating(image, db)
        return rating

    @staticmethod
    async def delete(rating_id: int, user, db: AsyncSession):
        rating = await db.scalar(
            select(Rating).where(
                (Rating.owner_id == user.id) & (Rating.id == rating_id)
            )
        )
        if not rating:
            return None
        await db.delete(rating)
        await db.commit()
        image = await ImageQuery.read(rating.image_id, db)
        await RatingQuery._update_average_rating(image, db)
        return rating
