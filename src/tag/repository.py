# tag related queries here
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import Tag

def __init__(self, db: AsyncSession):
        self.db = db

async def create_tag(self, tag_data):
    tag = Tag(**tag_data)
    self.db.add(tag)
    await self.db.commit()
    await self.db.refresh(tag)
    return tag

async def delete_tag(self, tag):
        self.db.delete(tag)
        await self.db.commit()
