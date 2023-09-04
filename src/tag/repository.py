# tag related queries here
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import Tag, Image, User

class TagRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tag: Tag):
        self.session.add(tag)
        await self.session.commit()

    async def read(self, tag_id: int):
        return await self.session.query(Tag).filter(Tag.id == tag_id).first()
