# tag related queries here
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import Tag

class TagRepository:
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

async def get_posts_by_tag(self, tag_name: str):
    posts = await self.db.execute(
    self.db.query(Tag).filter(Tag.title.ilike(f"%{tag_name}%"))
    )
    return posts.fetchall()