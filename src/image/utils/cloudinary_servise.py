import PIL
import cloudinary.uploader
from fastapi import UploadFile
from src.config import settings
from src.database.sql.alchemy_models import User


cloudinary.config(
    cloud_name=settings.cloudinary_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
    secure=True
)


async def upload_image(image_file: UploadFile, user: User) -> str:
    result = cloudinary.uploader.upload(image_file.file)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{user.username}') \
        .build_url(width=250, height=250, crop='fill', version=result.get('version'))
    return src_url
