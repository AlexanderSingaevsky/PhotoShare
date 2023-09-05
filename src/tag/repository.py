# tag related queries here
from sqlalchemy import select, or_
from sqlalchemy.orm import relationship
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

    @staticmethod
    async def update(tag_id: int, tag_schema: TagSchemaUpdateRequest, session: AsyncSession) -> Tag:
        stmt = select(Tag).where(Tag.id == tag_id)
        tag = await session.execute(stmt)
        tag = tag.scalars().unique().one_or_none()
        if tag:
            tag.name = tag_schema.name  # Ваша схема оновлення може виглядати інакше
            await session.commit()
            await session.refresh(tag)
        return tag

    @staticmethod
    async def delete(tag_id: int, session: AsyncSession):
        stmt = select(Tag).where(Tag.id == tag_id)
        tag = await session.execute(stmt)
        tag = tag.scalars().unique().one_or_none()
        if tag:
            await session.delete(tag)
            await session.commit()

    @staticmethod
    async def search_tags(query: str, session: AsyncSession) -> relationship[Tag]:
        stmt = select(Tag).filter(or_(Tag.name.ilike(f"%{query}%")))
        tags = await session.execute(stmt)
        return tags.scalars().all()

