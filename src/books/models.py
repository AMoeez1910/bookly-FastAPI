import uuid
from datetime import datetime

from sqlalchemy import Column, String
from sqlmodel import Field, SQLModel


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: str = Field(
        sa_column=Column(String(36), nullable=False, primary_key=True),
        default_factory=lambda: str(uuid.uuid4()),
    )
    title: str
    author: str
    published_year: int
    page_count: int
    language: str
    publisher: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"Book(uid={self.uid}, title={self.title}, author={self.author})"
