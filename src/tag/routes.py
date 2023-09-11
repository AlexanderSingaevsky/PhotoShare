from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.postgres_conn import database
from src.database.sql.alchemy_models import User
from src.auth.service import current_active_user
from src.tag.schemas import TagSchemaRequest
from src.tag.repository import TagRepository
from src.image.repository import ImageQuery
from src.auth.utils.access import access_service
from src.database.sql.alchemy_models import  Image

router = APIRouter(prefix='/tag', tags=["tags"])


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_tag(tag_data: TagSchemaRequest, user: User = Depends(current_active_user), session: AsyncSession = Depends(database)):
    image = await ImageQuery.read(tag_data.image_id, session)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image does not exist!')
    access = access_service('can_add_tag', user, image)
    if not access.is_authorized:
        raise HTTPException(status_code=access.status_code, detail=access.detail)
    await TagRepository.create(image, tag_data, session)
    return {'detail': 'tags added'}


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tags(tag_data: TagSchemaRequest, user: User = Depends(current_active_user), session: AsyncSession = Depends(database)):
    image = await ImageQuery.read(tag_data.image_id, session)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image does not exist!')
    access = access_service('can_delete_tag', user, image)
    if not access.is_authorized:
        raise HTTPException(status_code=access.status_code, detail=access.detail)
    await TagRepository.delete(image, tag_data, session)

@router.get("/search")
async def search_images_by_tags(tag_name: str, session: AsyncSession = Depends(database)):
    tags = await TagRepository.search_tags(tag_name, session)
    if not tags:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tag not found')
    image_ids = [tag.image_id for tag in tags]
    images = await ImageQuery.search_images_by_tags(image_ids, session)
    return images