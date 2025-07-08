from fastapi import APIRouter

from src.db import SessionDep

from .schemas import UserCreate
from .service import AuthService

auth_router = APIRouter()
auth_service = AuthService()


@auth_router.post("/sign-up", status_code=201, response_model=UserCreate)
async def create_user_account(user_data: UserCreate, session: SessionDep):
    user = await auth_service.create_user(user_data, session)
    return user
