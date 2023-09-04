from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, datetime


class CommentSchema(BaseModel):
    user_id: int = Field(1, ge=1)
    picture_id: int = Field(1, ge=1)
    comment_text: str = Field('Text of your comment', min_length=8, max_length=150)


class CommentResponseSchema(BaseModel):
    id: int = 1
    user_id: int = 1
    picture_id: int = 1
    comment_text: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True


class CommentUpdateSchema(BaseModel):
    id: int = 1
    comment_text: str

    class Config:
        from_attributes: True


class CommentUpdateResponseSchema(BaseModel):
    id: int = 1
    comment_text: str
    updated_at: datetime
    detail: str = 'Comment updated'

    class Config:
        from_attributes: True


