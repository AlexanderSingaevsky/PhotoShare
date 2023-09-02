import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    access_level: int


class UserCreate(schemas.BaseUserCreate):
    username: str
    access_level: int


class UserUpdate(UserCreate):
    pass