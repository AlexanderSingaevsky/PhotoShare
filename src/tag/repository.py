# tag related queries here
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import Tag, Image, ImageTag
from src.tag.schemas import TagSchemaRequest

class TagRepository:
    @staticmethod
    async def create(tag_schema: TagSchemaRequest, session: AsyncSession) -> Image:
        stmt = select(Image).where(Image.id == tag_schema.image_id)
        result = await session.execute(stmt)
        image = result.scalars().unique().one_or_none()
        if image:
            for tag in tag_schema.names:
                stmt = select(Tag).where(Tag.name == tag)
                tag_to_append = await session.execute(stmt)
                tag_to_append = tag_to_append.scalars().unique().one_or_none()
                if tag_to_append:
                    image.tags.append(tag_to_append)
                else:
                    image.tags.append(Tag(name=tag))
            session.add(image)
            await session.commit()
            await session.refresh(image)
        return image

    @staticmethod
    async def delete(tag_schema: TagSchemaRequest, session: AsyncSession) -> Image:
        stmt = select(Image).where(Image.id == tag_schema.image_id)
        result = await session.execute(stmt)
        image = result.scalars().unique().one_or_none()
        if image:
            for tag in image.tags:
                if tag.name in tag_schema.names:
                    image.tags.remove(tag)
            session.add(image)
            await session.commit()
        return image