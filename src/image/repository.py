from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import ImageResponse
class ImageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_image(self, image_data):
        image = ImageResponse(**image_data)
        self.db.add(image)
        await self.db.commit()
        await self.db.refresh(image)
        return image

    async def get_image(self, image_id):
        return await self.db.get(ImageResponse, image_id)

    async def update_image(self, image, image_update_data):
        for key, value in image_update_data.items():
            setattr(image, key, value)
        await self.db.commit()
        await self.db.refresh(image)
        return image

    async def delete_image(self, image):
        async with self.db.begin():
            self.db.delete(image)
            await self.db.flush()

    async def search_images(self, search_string):
        result = await self.db.execute(
            select(ImageResponse).filter(ImageResponse.title.ilike(f"%{search_string}%"))
        )
        return result.fetchall()
