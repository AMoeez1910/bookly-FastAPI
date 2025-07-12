import logging
from typing import List

from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel import select

from src.db import SessionDep, User

from ..db import is_jti_blocked
from .utils import decode_access_token


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)
        token = credentials.credentials
        token_data = decode_access_token(token)
        if not self.token_valid(token):
            raise HTTPException(
                status_code=403,
                detail="Invalid or expired access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if await is_jti_blocked(token_data["jti"]):
            raise HTTPException(
                status_code=403,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        try:
            payload = decode_access_token(token)
            return payload is not None
        except ValueError as e:
            logging.error(f"Token validation error: {str(e)}")
            return False

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError(
            "Subclasses must implement the verify_token_data method"
        )


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=403,
                detail="Access token is a refresh token, not an access token",
                headers={"WWW-Authenticate": "Bearer"},
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=403,
                detail="Access token is not a refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )


def get_current_logged_in_user(
    session: SessionDep, token_details: dict = Depends(AccessTokenBearer())
):
    user_email = token_details["user"]["email"]
    user = session.exec(select(User).where(User.email == user_email)).first()

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_logged_in_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to perform this action",
            )

        return True
