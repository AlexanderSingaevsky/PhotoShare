import uuid
from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID, SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import String, Integer, DateTime, Boolean, func, Uuid
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    access_level: Mapped[int] = mapped_column(Integer, ForeignKey('permissions.id'), default=1)
    permission = relationship("Permission", back_populates="users", lazy='joined')
    created_at: Mapped[DateTime] = mapped_column('crated_at', DateTime, default=func.now())
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship("OAuthAccount", lazy="joined")
    images = relationship("Image",  back_populates="owner", lazy='joined')


class Permission(Base):
    __tablename__ = 'permissions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    users: Mapped[User] = relationship("User", back_populates="permission", lazy='noload')
    role_name: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    can_add_image: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_update_image: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_delete_image: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_add_tag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_update_tag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_delete_tag: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_update_comment: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_delete_comment: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    picture_id: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_text: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column('created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)


class Image(Base):
    __tablename__ = 'images'
    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[User] = relationship("User", back_populates="images", lazy='noload')
    owner_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey('user.id'))
    title: Mapped[str] = mapped_column(String(30), nullable=True, default=None)
    cloudinary_url: Mapped[str] = mapped_column(String(300), nullable=False, default='placeholder')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=None, onupdate=func.now(), nullable=True)
