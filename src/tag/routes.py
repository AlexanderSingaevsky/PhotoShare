from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.postgres_conn import database
from src.tag.schemas import TagCreateRequest, TagDeleteRequest, TagSchemaResponse
from src.tag.repository import TagRepository

router = APIRouter(prefix='/tag', tags=["tags"])

@router.post("/create", response_model=TagSchemaResponse)
async def create_tag(tag_data: TagCreateRequest, session: AsyncSession = Depends(database)):
    # Перевірка, чи існує зображення з вказаним image_id
    image_exists = await TagRepository.check_image_exists(tag_data.image_id, session)
    if not image_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found.")
    
    # Додавання тегів до зображення
    created_tags = await TagRepository.create(tag_data, session)
    
    return created_tags

@router.delete("/delete", response_model=None)
async def delete_tags(tag_data: TagDeleteRequest, session: AsyncSession = Depends(database)):
    # Перевірка, чи існує зображення з вказаним image_id
    image_exists = await TagRepository.check_image_exists(tag_data.image_id, session)
    if not image_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found.")
    
    # Видалення тегів з зображення
    await TagRepository.delete_tags(tag_data, session)
    
    return None
