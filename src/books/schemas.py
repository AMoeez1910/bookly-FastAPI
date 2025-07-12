import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.schemas import UserAttributes


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    published_year: int
    page_count: int
    language: str
    publisher: str
    user_uid: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime
    user: Optional[UserAttributes]


class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int
    page_count: int
    language: str
    publisher: str


class BookAttributes(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    published_year: int
