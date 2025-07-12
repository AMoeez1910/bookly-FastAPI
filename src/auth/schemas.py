import uuid
from datetime import datetime

from pydantic import BaseModel, Field
from typing import List
from src.schemas import BookAttributes


class User(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    books: List[BookAttributes]


class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(min_length=6, max_length=128)
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=128)

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel


class UserAttributes(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_verified: bool | None = None

    class Config:
        from_attributes = True  # Enable ORM mode for compatibility with SQLModel
