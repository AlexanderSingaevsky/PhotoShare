from pydantic import BaseModel

# Модель для створення нової фотографії
class ImageCreate(BaseModel):
    title: str
    description: str

# Модель для оновлення опису фотографії
class ImageUpdate(BaseModel):
    description: str

# Модель для фотографії
class Image(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True