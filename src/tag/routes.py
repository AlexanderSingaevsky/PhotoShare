from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.postgres import database
from src.database.sql.models import User
from src.auth.service import current_active_user
from src.tag.schemas import TagSchemaRequest
from src.tag.repository import TagRepository
from src.image.routes import get_image
from src.auth.utils.access import access_service

router = APIRouter(prefix="/tag", tags=["tags"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagSchemaRequest,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(database),
):
    image = await get_image(tag_data.image_id, user, session)
    access_service("can_add_tag", user, image)
    await TagRepository.create(image, tag_data, session)
    return {"detail": "tags added"}


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tags(
    tag_data: TagSchemaRequest,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(database),
):
    image = await get_image(tag_data.image_id, user, session)
    access_service("can_delete_tag", user, image)
    await TagRepository.delete(image, tag_data, session)
