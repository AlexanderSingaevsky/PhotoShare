from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql.alchemy_models import User, Rating, Image


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
    async def create(body, user: User, db: AsyncSession) -> Rating:
        image = await db.get(Image, body.image_id)
        if not image:
            return None
        rating = Rating(**body.model_dump(), owner_id=user.id)
        db.add(rating)
        await db.commit()
        await db.refresh(rating)
        await RatingQuery._update_average_rating(image, db)
        return rating

    @staticmethod
    async def update(rating_id, body, db) -> Rating | None:
        sq = select(Rating).filter(Rating.id == rating_id)
        result = await db.execute(sq)
        rating = result.scalar_one_or_none()
        if rating:
            rating.value = body.value
            await db.commit()
            await db.refresh(rating)
            image = await db.get(Image, rating.image_id)
            await RatingQuery._update_average_rating(image, db)
        return rating

    # @staticmethod #TODO
    # async def delete(rating_id: int, db: AsyncSession) -> None:
    #     sq = select(Rating).filter_by(id=rating_id)
    #     result = await db.execute(sq)
    #     rating = result.scalar_one_or_none()
    #     if comment:
    #         await db.delete(rating)
    #         await db.commit()
