# src/shared/schemas.py
import uuid
from pydantic import BaseModel


class UserAttributes(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str


class BookAttributes(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    published_year: int
