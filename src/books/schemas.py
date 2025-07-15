import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from src.reviews import ReviewAttributes
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
    reviews: List[ReviewAttributes] = []


class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int
    page_count: int
    language: str
    publisher: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
    publisher: Optional[str] = None


class BookAttributes(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    published_year: int
