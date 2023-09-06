import hashlib
import cloudinary.uploader

from src.config import settings
from src.database.sql.alchemy_models import User


class UploadImage:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    @staticmethod
    def generate_name_folder(user: User):
        name = hashlib.sha256(user.email.encode('utf-8')).hexdigest()[:12]
        return f"Memento/{user.username}/{name}"

    @staticmethod
    def upload(file, public_id: str):
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_pic_url(public_id, r):
        src_url = cloudinary.CloudinaryImage(public_id).build_url(crop='fill', version=r.get('version'))
        return src_url