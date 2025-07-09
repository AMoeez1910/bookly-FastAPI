import logging
import uuid
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

from src.config import Config

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRY = 20


def generate_password_hash(password: str) -> str:
    """Generate a hashed password."""
    return passwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return passwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}
    payload["user"] = user_data
    payload["exp"] = (
        datetime.now()
        + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    ).timestamp()
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return token


# idea is that access token is for short time
# and refresh token is for longer time and used to get new access token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token, key=Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
