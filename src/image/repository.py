import os
import qrcode
import cloudinary
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql.models import Image, User, QRcode
from src.image.schemas import ImageSchemaUpdateRequest
from src.image.utils.cloudinary_service import init_cloudinary


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

    @staticmethod
    async def get_qr_url(photo_id: int, db: AsyncSession):
        query = select(Image).filter(Image.id == photo_id)
        result = await db.execute(query)
        photo = result.scalar()
        if photo is None:
            raise HTTPException(status_code=404)
        query = select(QRcode).filter(QRcode.photo_id == photo_id)
        result = await db.execute(query)
        qr = result.scalar_one_or_none()
        if qr is None:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(photo.cloudinary_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            qr_code_file_path = "my_qr_code.png"
            img.save(qr_code_file_path)

            init_cloudinary()
            upload_result = cloudinary.uploader.upload(
                qr_code_file_path,
                public_id=f"Qr_Code/Photo_{photo_id}",
                overwrite=True,
                invalidate=True,
            )
            qr = QRcode(url=upload_result["secure_url"], photo_id=photo_id)

            try:
                db.add(qr)
                await db.commit()
                await db.refresh(qr)
            except Exception as e:
                await db.rollback()
                raise e

            os.remove(qr_code_file_path)
            return {"source_url": photo.cloudinary_url, "qr_code_url": qr.url}

        return {"source_url": photo.cloudinary_url, "qr_code_url": qr.url}
