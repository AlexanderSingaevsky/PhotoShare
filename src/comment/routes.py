from fastapi import APIRouter, Path, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.alchemy_models import User
from src.auth.service import current_active_user
from src.comment.repository import CommentQuery
from src.comment.schemas import CommentSchemaRequest, CommentSchemaResponse, CommentUpdateSchemaRequest

from src.database.sql.postgres_conn import database

router = APIRouter(prefix="/comment", tags=["comments"])


@router.post('/create', name="Create new comment", response_model=CommentSchemaResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(body: CommentSchemaRequest,
                         user: User = Depends(current_active_user),
                         db: AsyncSession = Depends(database)):
    comment = await CommentQuery.create(body, user,  db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image does not exist!')
    return comment


@router.get('/{comment_id}', response_model=CommentSchemaResponse)
async def get_comment(comment_id: int = Path(ge=1), user: User = Depends(current_active_user), db: AsyncSession = Depends(database)):
    comment = await CommentQuery.read(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found!')
    return comment


@router.put('/update/{comment_id}', response_model=CommentSchemaResponse)
async def update_comment(comment_id: int,
                         body: CommentUpdateSchemaRequest,
                         user: User = Depends(current_active_user),
                         db: AsyncSession = Depends(database)):
    comment = await CommentQuery.update(comment_id, body, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment not found!')
    return comment


@router.delete('/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int = Path(ge=1),
                         user: User = Depends(current_active_user),
                         db: AsyncSession = Depends(database)):
    await CommentQuery.delete(comment_id, db)
