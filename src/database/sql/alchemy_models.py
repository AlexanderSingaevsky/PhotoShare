from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import TYPE_CHECKING, Generic, List

from fastapi_users.models import ID
from sqlalchemy import Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserFastapiUsersCustom(Generic[ID]):
    __tablename__ = "user"

    if TYPE_CHECKING:  # pragma: no cover
        id: int
        email: str
        username: str
        hashed_password: str
        avatar: str
        is_active: bool
        is_verified: bool

    else:
        id: Mapped[int] = mapped_column(
            Integer, primary_key=True, index=True, autoincrement=True
        )
        email: Mapped[str] = mapped_column(
            String(length=150), unique=True, nullable=False
        )
        username: Mapped[str] = mapped_column(
            String(length=26), unique=True, nullable=False
        )
        hashed_password: Mapped[str] = mapped_column(
            String(length=150), nullable=False
        )
        avatar: Mapped[str] = mapped_column(String(255), nullable=True)
        is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
        is_verified: Mapped[bool] = mapped_column(
            Boolean, default=False, nullable=False
        )


class User(UserFastapiUsersCustom[int], Base):
    pass
