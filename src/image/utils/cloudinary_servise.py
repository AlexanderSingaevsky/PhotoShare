import PIL
import cloudinary.uploader
from fastapi import UploadFile

# Конфігурація Cloudinary
cloudinary.config(
    cloud_name="CLOUDINARY_CLOUD_NAME",
    api_key="CLOUDINARY_API_KEY",
    api_secret="CLOUDINARY_API_SECRET"
)

# Функція для завантаження зображення на Cloudinary
async def upload_image(image_file: UploadFile):
    # Завантаження зображення на Cloudinary
    result = cloudinary.uploader.upload(image_file.file)  # image_file.file містить байти зображення

    # Повертаємо публічний URL завантаженого зображення
    return result["secure_url"]


async def valid_image_file(file: UploadFile) -> bool:
    try:
        # Спробуємо відкрити файл за допомогою бібліотеки PIL
        image = PIL.Image.open(file.file)
        return True
    except (OSError, IOError, ValueError) as e:
        # Файл не є дійсним файлом зображення
        return False