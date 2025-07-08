from datetime import timedelta

import jwt
from passlib.context import CryptContext

from src.config import Config

from .schemas import User

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    """Generate a hashed password."""
    return passwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return passwd_context.verify(plain_password, hashed_password)


def create_access_token(user_data: User, expiry: timedelta):
    payload = {}
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
