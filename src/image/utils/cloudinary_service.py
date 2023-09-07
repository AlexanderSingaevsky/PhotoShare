import hashlib
import re
import uuid
from datetime import datetime

import cloudinary.uploader

from src.config import settings
from src.database.sql.alchemy_models import User
from src.image.schemas import ImageSchemaOnEditRequest


class UploadImage:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    @staticmethod
    def generate_name_folder(user: User):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d-%m-%Y")
        return f"Memento/{user.username}/{formatted_date}/{str(uuid.uuid4())}"

    @staticmethod
    def upload(file, public_id: str):
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_pic_url(public_id, r):
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            # version=r.get("version")
        )
        return src_url

    @staticmethod
    def edit_image(original_img_url: str, edit_data: ImageSchemaOnEditRequest):
        match = re.search(r"Memento/(\w+)/(\d{2}-\d{2}-\d{4})/(.*)", original_img_url)
        if match:
            public_id = match.group()
            print(public_id)
            if edit_data.ai_replace:
                image_edit = cloudinary.CloudinaryImage(public_id).image(
                    effect=f"gen_replace:from_{edit_data.ai_replace['Object to detect']};to_{edit_data.ai_replace['Replace with']}"
                )
            elif edit_data.scale:
                image_edit = cloudinary.CloudinaryImage(public_id).image(
                    width=edit_data.scale["Width"], height=edit_data.scale["Height"]
                )
            elif edit_data.black_and_white:
                image_edit = cloudinary.CloudinaryImage(public_id).image(
                    transformation=["blacknwite"]
                )
            elif edit_data.rotation:
                image_edit = cloudinary.CloudinaryImage(public_id).image(
                    angle=edit_data.rotation
                )
            elif edit_data.flip_mode:
                image_edit = cloudinary.CloudinaryImage(public_id).image(
                    angle=edit_data.flip_mode["flip_mode"]
                )
            print(
                "****4. Transform the image****\nTransfrmation URL: ", image_edit, "\n"
            )
            return image_edit
        # else:
        #     raise ValueError
