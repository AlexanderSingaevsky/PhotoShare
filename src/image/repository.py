from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql.alchemy_models import Image, User
from src.image.schemas import ImageSchemaRequest, ImageSchemaUpdateRequest


class ImageQuery:

    @staticmethod
    async def create(title: str, cloudinary_url: str, user: User, session: AsyncSession) -> Image:
        image = Image(title=title, owner_id=user.id, cloudinary_url=cloudinary_url)
        session.add(image)
        await session.commit()
        return image

    @staticmethod
    async def read(image_id: int, session: AsyncSession) -> Image| None:
        stmt = select(Image).where(Image.id == image_id)
        image = await session.execute(stmt)
        return image.scalars().unique().one_or_none()

    @staticmethod
    async def update(image_id: int, image_data: ImageSchemaUpdateRequest, session: AsyncSession) -> Image:
        stmt = select(Image).where(Image.id == image_id)
        image = await session.execute(stmt)
        image = image.scalars().unique().one_or_none()
        if image:
            image.title = image_data.title
            await session.commit()
            await session.refresh(image)
        return image

    @staticmethod
    async def delete(image_id: int, session: AsyncSession) -> None:
        stmt = select(Image).filter_by(id=image_id)
        result = await session.execute(stmt)
        image = result.scalar_one_or_none()
        if image:
            await session.delete(image)
            await session.commit()


