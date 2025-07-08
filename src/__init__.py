from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth import auth_router
from src.books import book_router
from src.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    version="v1",
    title="Bookly API",
    description="A simple API for managing books",
    lifespan=lifespan,
)


app.include_router(
    book_router,
    tags=["books"],
    prefix="/api/v1/books",
)


app.include_router(
    auth_router,
    tags=["auth"],
    prefix="/api/v1/auth",
)
