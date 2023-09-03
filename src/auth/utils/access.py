from fastapi import HTTPException, status

from src.database.sql.alchemy_models import User


class Image:
    owner_id = 1


class Tag:
    owner_id = 1


class Comment:
    owner_id = 1


class AccessService:
    async def __call__(self, action: str, user: User, item: Image | Tag | Comment | None = None) -> None:
        # add items when they will be ready
        if user.is_superuser or user.permission.__dict__.get(action, False):
            return None
        elif not user.is_verified:
            # move raise to routes (or maybe not)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail=f'Email is not verified. Please varify your email: {user.email}.')
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f'You are not allowed to do this operation')


access_service = AccessService()
