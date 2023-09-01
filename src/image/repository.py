from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import DBImage
class ImageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_image(self, image_data):
        image = DBImage(**image_data)
        self.db.add(image)
        await self.db.commit()
        await self.db.refresh(image)
        return image

    async def get_image(self, image_id):
        return await self.db.get(DBImage, image_id)

    async def update_image(self, image, image_update_data):
        for key, value in image_update_data.items():
            setattr(image, key, value)
        await self.db.commit()
        await self.db.refresh(image)
        return image

    async def delete_image(self, image):
        self.db.delete(image)
        await self.db.commit()

    async def search_images(self, search_string):
        images = await self.db.execute(
            self.db.query(DBImage).filter(DBImage.title.ilike(f"%{search_string}%"))
        )
        return images.fetchall()
