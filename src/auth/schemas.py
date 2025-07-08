import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str = Field(min_length=6, max_length=128)
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_verified: bool | None = None

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLModel
