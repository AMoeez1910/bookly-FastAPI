from typing import List

from fastapi import APIRouter, Depends

from src.auth import RoleChecker
from src.db import SessionDep

from ..auth import AccessTokenBearer
from .schemas import Book as BookSchema
from .schemas import BookCreate, BookUpdate
from .service import BookService

book_router = APIRouter()

book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@book_router.get(
    "/",
    response_model=List[BookSchema],
    dependencies=[role_checker, Depends(access_token_bearer)],
)
async def get_books(session: SessionDep):
    return await book_service.get_all_books(session)


@book_router.get(
    "/{book_id}", dependencies=[role_checker, Depends(access_token_bearer)]
)
async def get_book_by_id(book_id: str, session: SessionDep):
    """
    Retrieve a book by its ID.
    """
    return await book_service.get_book_by_id(book_id, session)


@book_router.post("", status_code=201, dependencies=[role_checker])
async def create_book(
    book: BookCreate,
    session: SessionDep,
    token_details: dict = Depends(access_token_bearer),
):
    """
    Create a new book.
    """

    user_uid = token_details["user"]["uid"]

    return await book_service.create_book(
        book_data=book,
        session=session,
        user_uid=user_uid,
    )


@book_router.patch(
    "/{book_id}", dependencies=[role_checker, Depends(access_token_bearer)]
)
async def update_book_partial(
    book_id: str,
    book: BookUpdate,
    session: SessionDep,
):
    """
    Partially update an existing book by its ID.
    """
    return await book_service.update_book(book_id, book, session)


@book_router.delete(
    "/{book_id}",
    status_code=204,
    dependencies=[role_checker, Depends(access_token_bearer)],
)
async def delete_book(book_id: str, session: SessionDep):
    """
    Delete a book by its ID.
    """
    return await book_service.delete_book(book_id, session)


# , token_details: dict = Depends(access_token_bearer)
