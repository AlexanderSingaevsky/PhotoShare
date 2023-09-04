from fastapi import HTTPException, status

from src.database.sql.alchemy_models import User


class Image:
    owner_id = 1


class Tag:
    owner_id = 1


class Comment:
    owner_id = 1


class PermissionStatus:
    __slots__ = ['is_authorized', "status_code", "detail"]

    def __init__(self, is_authorized: bool, status_code: int, detail: str):
        self.is_authorized = is_authorized
        self.status_code = status_code
        self.detail = detail


class Item:
    owner_id = 1


class AccessService:
    async def __call__(self, action: str, user: User, item: Image | Tag | Comment | None = None) -> PermissionStatus:
        if item is None:
            item = Item()

        if not user.is_verified:
            detail = f'Email is not verified. Please varify your email: {user.email}.'
            return PermissionStatus(False, status.HTTP_422_UNPROCESSABLE_ENTITY, detail)
        elif user.is_superuser or user.permission.__dict__.get(action, False) or user.id == item.owner_id:
            detail = "Access Granted!"
            return PermissionStatus(True, status.HTTP_200_OK, detail)
        else:
            detail = f'You are not allowed to do this operation'
            return PermissionStatus(False, status.HTTP_403_FORBIDDEN, detail)


access_service = AccessService()
