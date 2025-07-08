from fastapi import HTTPException
from sqlmodel import select

from src.db import SessionDep

from .models import Book
from .schemas import BookCreate


class BookService:
    async def get_all_books(self, session: SessionDep):
        books = session.exec(select(Book)).all()
        return books

    async def get_book_by_id(self, book_id: str, session: SessionDep):
        book = session.exec(select(Book).where(Book.uid == book_id)).first()
        if not book:
            raise HTTPException(
                status_code=404, detail=f"Book with id {book_id} not found"
            )
        return book

    async def create_book(self, book_data: BookCreate, session: SessionDep):
        book = Book(**book_data.model_dump())
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    async def update_book(
        self, book_id: str, book_data: BookCreate, session: SessionDep
    ):
        book = session.get(Book, book_id)

        if not book:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = book_data.model_dump(exclude_unset=True)
        book.sqlmodel_update(hero_data)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    async def delete_book(self, book_id: str, session: SessionDep):
        book = session.get(Book, book_id)
        if not book:
            raise HTTPException(
                status_code=404, detail=f"Book with id {book_id} not found"
            )
        session.delete(book)
        session.commit()
        return {"detail": f"Book with id {book_id} deleted successfully"}
