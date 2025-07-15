import uuid
from datetime import datetime

from pydantic import BaseModel


class ReviewModel(BaseModel):
    uid: uuid.UUID
    book_uid: uuid.UUID
    user_uid: uuid.UUID
    rating: int
    comment: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    rating: int
    comment: str

    class Config:
        from_attributes = True


class ReviewUpdate(BaseModel):
    rating: int | None = None
    comment: str | None = None

    class Config:
        from_attributes = True


class ReviewAttributes(BaseModel):
    uid: uuid.UUID
    book_uid: uuid.UUID
    user_uid: uuid.UUID
    rating: int
    comment: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
