from typing import List

from fastapi import APIRouter, Path, Depends, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import User
from src.auth.service import current_active_user
from ..comment import repository as comments_repo
from src.comment.schemas import CommentResponseSchema, CommentUpdateResponseSchema, CommentUpdateSchema, CommentSchema
from src.database.sql.postgres_conn import database

router = APIRouter(prefix="/comment", tags=["comments"])


@router.get('/', name='Get all comments', response_model=List[CommentResponseSchema])
async def get_all_comments(limit: int = Query(default=10, le=200), db: AsyncSession = Depends(database), user: User = Depends(current_active_user)):
    comments = await comments_repo.get_all_comments(db, limit)
    return comments


@router.get('/{comment_id}', name='Get one comment', response_model=CommentResponseSchema)
async def get_one_comment(comment_id: int = Path(ge=1), db: AsyncSession = Depends(database), user: User = Depends(current_active_user)):
    comment = await comments_repo.get_one_comment(comment_id, db)
    return comment


@router.post('/', name="Create new comment", response_model=CommentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(body: CommentSchema, db: AsyncSession = Depends(database), user: User = Depends(current_active_user)):
    comment = await comments_repo.create_new_comment(body, db)
    return comment


@router.put('/', name="Update existing comment", response_model=CommentUpdateResponseSchema,
            status_code=status.HTTP_200_OK)
async def update_comment(body: CommentUpdateSchema, db: AsyncSession = Depends(database), user: User = Depends(current_active_user)):
    comment = await comments_repo.update_comment(body, db)
    return comment


@router.delete('/{comment_id}', name="Delete existing comment", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int = Path(ge=1), db: AsyncSession = Depends(database), user: User = Depends(current_active_user)):
    await comments_repo.remove_comment(comment_id, db)
    return JSONResponse(content={"detail": f"Comment {comment_id} deleted!"})
