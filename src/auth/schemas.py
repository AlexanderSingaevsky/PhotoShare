from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    username: str


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(min_length=5, max_length=26)


class UserUpdate(schemas.BaseUserUpdate):
    pass
