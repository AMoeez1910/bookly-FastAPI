import uuid
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    first_name: str
    last_name: str
    # not shown in responses
    password_hash: str = Field(exclude=True)
    role: str = Field(default="user", index=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    books: List["Book"] = Relationship(back_populates="user")
    reviews: List["Reviews"] = Relationship(back_populates="user")

    def __repr__(self):
        return f"User(uid={self.uid}, username={self.username}, email={self.email})"


class Book(SQLModel, table=True):
    __tablename__ = "books"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    title: str
    author: str
    published_year: int
    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="users.uid",
    )
    page_count: int
    language: str
    publisher: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    user: Optional["User"] = Relationship(back_populates="books")
    reviews: List["Reviews"] = Relationship(back_populates="book")

    def __repr__(self):
        return f"Book(uid={self.uid}, title={self.title}, author={self.author})"


class Reviews(SQLModel, table=True):
    __tablename__ = "reviews"
    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    book_uid: uuid.UUID = Field(foreign_key="books.uid", nullable=False)
    user_uid: uuid.UUID = Field(foreign_key="users.uid", nullable=False)
    rating: int = Field(ge=1, le=5)  # Rating between 1 and 5
    comment: Optional[str] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    book: Optional[Book] = Relationship(back_populates="reviews")
    user: Optional[User] = Relationship(back_populates="reviews")
