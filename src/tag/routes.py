from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.postgres_conn import database
from src.database.cache.redis_conn import cache_database
from src.tag.schemas import TagCreate, TagUpdate, Tag
from src.tag.repository import TagRepository
from src.image.repository import ImageRepository

router = APIRouter(prefix='/tag', tags=["tags"])

@router.post("/", response_model=Tag)
async def create_tag(tag_data: TagCreate, session: AsyncSession = Depends(database.get_session)):
    async with session.begin():
        tag = await TagRepository.create(tag_data.dict(), session)
        return tag

@router.get("/{tag_id}", response_model=Tag)
async def read_tag(tag_id: int, session: AsyncSession = Depends(database.get_session)):
    tag = await TagRepository.read(tag_id, session)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.put("/{tag_id}", response_model=Tag)
async def update_tag(tag_id: int, tag_data: TagUpdate, session: AsyncSession = Depends(database.get_session)):
    async with session.begin():
        tag = await TagRepository.update(tag_id, tag_data.dict(), session)
        if tag is None:
            raise HTTPException(status_code=404, detail="Tag not found")
        return tag

@router.delete("/{tag_id}", response_model=None)
async def delete_tag(tag_id: int, session: AsyncSession = Depends(database.get_session)):
    async with session.begin():
        tag = await TagRepository.delete(tag_id, session)
        if tag is None:
            raise HTTPException(status_code=404, detail="Tag not found")
