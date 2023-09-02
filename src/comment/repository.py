# comment related queries here
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.sql.alchemy_models import Comment


async def create_new_comment(body, db: AsyncSession):
    comment = Comment(**body.model_dump())
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def get_one_comment(comment_id: int, db: AsyncSession):
    sq = select(Comment).filter_by(id=comment_id)
    comment = await db.execute(sq)
    existing_comment = comment.scalar_one_or_none()
    if existing_comment:
        return existing_comment
    raise HTTPException(status_code=404, detail="Comment not found")


async def get_all_comments(db, limit):
    sq = select(Comment).limit(limit)
    print(sq)
    comments = await db.execute(sq)
    return comments.scalars().all()


async def update_comment(db, limit):
    sq = select(Comment).limit(limit)
    print(sq)
    comments = await db.execute(sq)
    return comments.scalars().all()


async def update_comment(body, db):
    sq = select(Comment).filter_by(id=body.id)
    comment = await db.execute(sq)
    existing_comment = comment.scalar_one_or_none()
    if existing_comment:
        existing_comment.comment_text = body.comment_text
        await db.commit()
        await db.refresh(existing_comment)
        return existing_comment
    raise HTTPException(status_code=404, detail="Comment not found")


async def remove_comment(comment_id: int, db: AsyncSession):
    sq = select(Comment).filter_by(id=comment_id)
    result = await db.execute(sq)
    comment_to_delete = result.scalar_one_or_none()
    if not comment_to_delete:
        raise HTTPException(status_code=404, detail="Comment not found")
    await db.delete(comment_to_delete)
    await db.commit()
