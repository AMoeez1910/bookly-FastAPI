from typing import List

from fastapi import APIRouter

from src.db import SessionDep

from .schemas import Book as BookSchema
from .schemas import BookCreate
from .service import BookService

book_router = APIRouter()

book_service = BookService()


@book_router.get("/", response_model=List[BookSchema])
async def get_books(session: SessionDep):
    return await book_service.get_all_books(session)


@book_router.get("/{book_id}")
async def get_book_by_id(book_id: str, session: SessionDep):
    """
    Retrieve a book by its ID.
    """
    return await book_service.get_book_by_id(book_id, session)


@book_router.post("", status_code=201)
async def create_book(book: BookCreate, session: SessionDep):
    """
    Create a new book.
    """
    return await book_service.create_book(book, session)


@book_router.patch("/{book_id}")
async def update_book_partial(book_id: str, book: BookCreate, session: SessionDep):
    """
    Partially update an existing book by its ID.
    """
    return await book_service.update_book(book_id, book, session)


@book_router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: str, session: SessionDep):
    """
    Delete a book by its ID.
    """
    return await book_service.delete_book(book_id, session)
