import hashlib
import re
import uuid
from datetime import datetime
from typing import Union

import cloudinary.uploader

from src.config import settings
from src.database.sql.alchemy_models import User
from src.image.schemas import (
    ImageAIReplaceTransformation,
    ImageScaleTransformation,
    ImageBlackAndWhiteTransformation,
    ImageRotationTransformation,
    ImageFlipModeTransformation,
)


class UploadImage:
    def __init__(self):
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


class ImageEditor(UploadImage):
    async def edit_image(
        self,
        original_img_url: str,
        edit_data: Union[
            ImageScaleTransformation,
            ImageAIReplaceTransformation,
            ImageBlackAndWhiteTransformation,
            ImageRotationTransformation,
            ImageFlipModeTransformation,
        ],
    ):
        match = re.search(r"Memento/(.*)/(\d{2}-\d{2}-\d{4})/(.*)", original_img_url)
        if not match:
            raise ValueError("Invalid URL format")

        public_id = match.group()  # Отримуємо перший підшаблон (групу)
        print(public_id)

        # Словник з функціями трансформації
        transformation_functions = {
            ImageScaleTransformation: self._edit_image_with_scale,
            ImageAIReplaceTransformation: self._edit_image_with_ai_replace,
            ImageBlackAndWhiteTransformation: self._edit_image_black_and_white,
            ImageRotationTransformation: self._edit_image_with_rotation,
            ImageFlipModeTransformation: self._edit_image_with_flip_mode,
        }

        for (
            transformation_type,
            transformation_function,
        ) in transformation_functions.items():
            if isinstance(edit_data, transformation_type):
                image_edit_html = await transformation_function(public_id, edit_data)
                pattern2 = re.search(r'src="([^"]+)"', image_edit_html)
                image_edit = pattern2.group(1)
                print(pattern2.group(1))
                return image_edit

        raise ValueError("No transformation specified")

    async def _edit_image_with_ai_replace(
        self, public_id, ai_replace: ImageAIReplaceTransformation
    ):
        return cloudinary.CloudinaryImage(public_id).image(
            effect=f"gen_replace:from_{ai_replace.Object_to_detect};to_{ai_replace.Replace_with}"
        )

    async def _edit_image_with_scale(self, public_id, scale: ImageScaleTransformation):
        return cloudinary.CloudinaryImage(public_id).image(
            width=scale.Width, height=scale.Height
        )

    async def _edit_image_black_and_white(
        self, public_id, black_and_white: ImageBlackAndWhiteTransformation
    ):
        if black_and_white.black_and_white:
            pass
        return cloudinary.CloudinaryImage(public_id).image(
            transformation=["blacknwite"]
        )

    async def _edit_image_with_rotation(
        self, public_id, rotation: ImageRotationTransformation
    ):
        return cloudinary.CloudinaryImage(public_id).image(angle=rotation.angle)

    async def _edit_image_with_flip_mode(
        self, public_id, flip_mode: ImageFlipModeTransformation
    ):
        return cloudinary.CloudinaryImage(public_id).image(angle=flip_mode.flip_mode)

    # @staticmethod
    # def edit_image(original_img_url: str, edit_data: ImageSchemaOnEditRequest):
    #     match = re.search(r"Memento/(.*)/(\d{2}-\d{2}-\d{4})/(.*)", original_img_url)
    #     if match:
    #         public_id = match.group()
    #         print(public_id)
    #         if edit_data.ai_replace:
    #             image_edit = cloudinary.CloudinaryImage(public_id).image(
    #                 effect=f"gen_replace:from_{edit_data.ai_replace['Object to detect']};to_{edit_data.ai_replace['Replace with']}"
    #             )
    #         elif edit_data.scale:
    #             image_edit = cloudinary.CloudinaryImage(public_id).image(
    #                 width=edit_data.scale["Width"], height=edit_data.scale["Height"]
    #             )
    #         elif edit_data.black_and_white:
    #             image_edit = cloudinary.CloudinaryImage(public_id).image(
    #                 transformation=["blacknwite"]
    #             )
    #         elif edit_data.rotation:
    #             image_edit = cloudinary.CloudinaryImage(public_id).image(
    #                 angle=edit_data.rotation
    #             )
    #         elif edit_data.flip_mode:
    #             image_edit = cloudinary.CloudinaryImage(public_id).image(
    #                 angle=edit_data.flip_mode["flip_mode"]
    #             )
    #         print(
    #             "****4. Transform the image****\nTransfrmation URL: ", image_edit, "\n"
    #         )
    #         return image_edit
    #
    #     # else:
    #     #     raise ValueError
