# tag related queries here
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import Tag


class TagRepository:
    async def create_tag(self, tag_data):
        pass

    async def delete_tag(self, tag):
        pass

    async def get_posts_by_tag(self, tag_name: str):
        pass
