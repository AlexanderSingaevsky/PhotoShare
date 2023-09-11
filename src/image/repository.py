from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql.alchemy_models import Image, User
from src.image.schemas import ImageSchemaUpdateRequest


class ImageQuery:
    @staticmethod
    async def create(
        title: str, cloudinary_url: str, user: User, session: AsyncSession
    ) -> Image:
        image = Image(title=title, owner_id=user.id, cloudinary_url=cloudinary_url)
        session.add(image)
        await session.commit()
        return image

    @staticmethod
    async def read(image_id: int, session: AsyncSession) -> Image | None:
        stmt = select(Image).where(Image.id == image_id)
        image = await session.execute(stmt)
        return image.scalars().unique().one_or_none()

    @staticmethod
    async def update(
        image: Image,
        session: AsyncSession,
        edited_cloudinary_url: str = None,
        image_data: ImageSchemaUpdateRequest = None,
    ) -> Image:

        if image_data:
            image.title = image_data.title
        if edited_cloudinary_url:
            image.edited_cloudinary_url = edited_cloudinary_url
        await session.commit()
        await session.refresh(image)
        return image

    @staticmethod
    async def delete(image: Image, session: AsyncSession) -> None:
        await session.delete(image)
        await session.commit()

