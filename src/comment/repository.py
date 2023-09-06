# comment related queries here
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql.alchemy_models import Comment, User


class CommentQuery:
    @staticmethod
    async def create(body, user: User, db: AsyncSession) -> Comment:
        comment = Comment(**body.model_dump(), owner_id=user.id)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def read(comment_id: int, db: AsyncSession) -> Comment | None:
        sq = select(Comment).filter_by(id=comment_id)
        comment = await db.execute(sq)
        comment = comment.scalar_one_or_none()
        return comment

    @staticmethod
    async def update(comment_id, body, db) -> Comment | None:
        sq = select(Comment).filter_by(id=comment_id)
        result = await db.execute(sq)
        comment = result.scalar_one_or_none()
        if comment:
            comment.text = body.text
            await db.commit()
            await db.refresh(comment)
        return comment

    @staticmethod
    async def delete(comment_id: int, db: AsyncSession) -> None:
        sq = select(Comment).filter_by(id=comment_id)
        result = await db.execute(sq)
        comment = result.scalar_one_or_none()
        if comment:
            await db.delete(comment)
            await db.commit()

