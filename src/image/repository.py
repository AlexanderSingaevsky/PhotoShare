from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql.alchemy_models import Image, User
from src.image.schemas import ImageSchemaRequest, ImageSchemaUpdateRequest
from src.image.utils.cloudinary_servise import upload_image, valid_image_file


class ImageQuery:

    @staticmethod
    async def create(image_data: ImageSchemaRequest, user: User, session: AsyncSession, image_file: UploadFile) -> Image:
        if not valid_image_file(image_file):
            raise HTTPException(status_code=422, detail="Invalid image file")
        # Завантажуємо зображення на Cloudinary
        cloudinary_url = await upload_image(image_data.file)  # Передаємо файл зображення
        image = Image(**image_data.model_dump(), owner_id=user.id, cloudinary_url=cloudinary_url)
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


