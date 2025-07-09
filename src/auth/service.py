from datetime import timedelta

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select

from src.db import SessionDep

from .models import User
from .schemas import UserCreate, UserLogin, UserUpdate
from .utils import create_access_token, generate_password_hash, verify_password


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

    async def login_user(self, user_data: UserLogin, session: SessionDep):
        """
        Authenticate a user by email and password.
        """
        user = await self.get_user(user_data.email, session)

        if user is not None:
            password_matches = verify_password(user_data.password, user.password_hash)
            if password_matches:
                access_token = create_access_token(
                    user_data={
                        "uid": str(user.uid),
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_verified": user.is_verified,
                    }
                )
                refresh_token = create_access_token(
                    user_data={
                        "uid": str(user.uid),
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_verified": user.is_verified,
                    },
                    expiry=timedelta(days=30),
                    refresh=True,
                )
                return JSONResponse(
                    content={
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "message": "Login successful",
                        "user": {
                            "uid": str(user.uid),
                            "username": user.username,
                            "email": user.email,
                            "first_name": user.first_name,
                            "last_name": user.last_name,
                            "is_verified": user.is_verified,
                            "created_at": user.created_at.isoformat(),
                            "updated_at": user.updated_at.isoformat(),
                        },
                    }
                )
            else:
                raise HTTPException(status_code=403, detail="Invalid credentials")
        else:
            raise HTTPException(status_code=403, detail="Invalid credentials")
