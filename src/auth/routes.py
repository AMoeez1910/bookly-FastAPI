from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from src.auth.utils import create_access_token
from src.db import SessionDep

from .dependencies import RefreshTokenBearer
from .schemas import User, UserCreate, UserLogin
from .service import AuthService

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post("/sign-up", status_code=201, response_model=User)
async def create_user_account(user_data: UserCreate, session: SessionDep):
    user = await auth_service.create_user(user_data, session)
    return user


@auth_router.post("/login")
async def login_user(user_data: UserLogin, session: SessionDep):
    return await auth_service.login_user(user_data, session)


@auth_router.get("/refresh-token")
async def refresh_token(token_details: dict = Depends(RefreshTokenBearer())):
    print(token_details)
    token_expiry: datetime = token_details["exp"]

    print(datetime.fromtimestamp(token_expiry))
    if datetime.fromtimestamp(token_expiry) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details["user"]
        )
        return {"access_token": new_access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=401, detail="Refresh token has expired or is invalid"
    )
