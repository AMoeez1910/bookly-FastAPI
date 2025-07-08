from fastapi import HTTPException
from sqlmodel import select

from src.db import SessionDep

from .models import User
from .schemas import UserCreate, UserUpdate
from .utils import generate_password_hash


class AuthService:
    async def get_user(self, email: str, session: SessionDep):
        """
        Retrieve a user by their email.
        """
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            return None
        return user

    async def user_exists(self, email: str, session: SessionDep):
        user = await self.get_user(email, session)
        return user is not None

    async def create_user(self, user_data: UserCreate, session: SessionDep):
        """
        Create a new user.
        """
        if await self.user_exists(user_data.email, session):
            raise HTTPException(status_code=400, detail="User already exists")
        hash_password = generate_password_hash(user_data.password)
        user = User(**user_data.model_dump())
        user.password_hash = hash_password
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    async def update_user(
        self, user_id: str, user_data: UserUpdate, session: SessionDep
    ):
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data_dict = user_data.model_dump(exclude_unset=True)
        user.sqlmodel_update(user_data_dict)
        session.add(user)
        session.commit()
        session.refresh(user)

        return user
