from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.db import SessionDep

from ..db import add_jti_to_blocklist
from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    get_current_logged_in_user,
)
from .schemas import User, UserBookModel, UserCreate, UserLogin
from .service import AuthService
from .utils import create_access_token

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
    token_expiry: datetime = token_details["exp"]
    if datetime.fromtimestamp(token_expiry) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])
        return {"access_token": new_access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=401, detail="Refresh token has expired or is invalid"
    )


@auth_router.get("/logout", status_code=204)
async def logout_user(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    if not jti:
        raise HTTPException(status_code=400, detail="Invalid token")
    await add_jti_to_blocklist(jti)
    return JSONResponse(status_code=204, content={"message": "Successfully logged out"})


@auth_router.get("/user", response_model=UserBookModel)
async def get_current_user(user_details=Depends(get_current_logged_in_user)):
    return user_details
