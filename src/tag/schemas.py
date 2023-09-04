from pydantic import BaseModel


class TagCreate(BaseModel):
    title: str
    description: str


class TagUpdate(BaseModel):
    description: str


class Tag(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True