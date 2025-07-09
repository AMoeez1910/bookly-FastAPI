import logging

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from .utils import decode_access_token


class TokenBearer(HTTPBearer):
    def _init(self, auto_error=True):
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

        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        try:
            payload = decode_access_token(token)
            if payload is None:
                return False
            return True
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
