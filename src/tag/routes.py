from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.sql.postgres_conn import database
from src.tag.schemas import TagSchemaRequest, TagSchemaResponse, TagSchemaUpdateRequest
from src.tag.repository import TagRepository

router = APIRouter(prefix='/tag', tags=["tags"])


@router.post("/create", response_model=TagSchemaResponse)
async def create_tag(tag_data: TagSchemaRequest, session: AsyncSession = Depends(database)):
    tag = await TagRepository.create(tag_data, session)
    return tag


@router.get("/{tag_id}", response_model=TagSchemaResponse)
async def read_tag(tag_id: int, session: AsyncSession = Depends(database)):
    tag = await TagRepository.read(tag_id, session)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found.")
    return tag


# @router.put("/{tag_id}", response_model=TagSchemaResponse)
# async def update_tag(tag_id: int, tag_data: TagUpdate, session: AsyncSession = Depends(database.get_session)):
#     async with session.begin():
#         tag = await TagRepository.update(tag_id, tag_data.dict(), session)
#         if tag is None:
#             raise HTTPException(status_code=404, detail="Tag not found")
#         return tag
#
#
# @router.delete("/{tag_id}", response_model=None)
# async def delete_tag(tag_id: int, session: AsyncSession = Depends(database.get_session)):
#     async with session.begin():
#         tag = await TagRepository.delete(tag_id, session)
#         if tag is None:
#             raise HTTPException(status_code=404, detail="Tag not found")
