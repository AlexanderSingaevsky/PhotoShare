from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.postgres_conn import database
from src.tag.schemas import TagSchemaRequest, TagSchemaResponse,TagSchemaUpdateRequest
from src.tag.repository import TagRepository

router = APIRouter(prefix='/tag', tags=["tags"])


@router.post("/create")
async def create_tag(tag_data: TagSchemaRequest, session: AsyncSession = Depends(database)):
    image_exists = await TagRepository.create(tag_data, session)
    if not image_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found.")
    return {'detail': 'tags added'}

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tags(tag_data: TagSchemaRequest, session: AsyncSession = Depends(database)):
    image_exists = await TagRepository.delete(tag_data, session)
    if not image_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found.")
