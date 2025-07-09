from datetime import datetime

from pydantic import BaseModel


class Book(BaseModel):
    uid: str
    title: str
    author: str
    published_year: int
    page_count: int
    language: str
    publisher: str
    created_at: datetime
    updated_at: datetime


class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int
    page_count: int
    language: str
    publisher: str
