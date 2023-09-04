# tag related queries here
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import Tag
from src.tag.schemas import TagSchemaRequest, TagSchemaResponse, TagSchemaUpdateRequest

class TagRepository:
    @staticmethod
    async def create(tag_schema: TagSchemaRequest, session: AsyncSession) -> Tag:
        tag = Tag(**tag_schema.model_dump())
        session.add(tag)
        await session.commit()
        await session.refresh(tag)
        return tag

    @staticmethod
    async def read(tag_id: int, session: AsyncSession):
        stmt = select(Tag).where(Tag.id == tag_id)
        tag = await session.execute(stmt)
        return tag.scalars().unique().one_or_none()

