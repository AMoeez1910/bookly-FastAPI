import uuid

from fastapi import HTTPException
from sqlmodel import select

from src.db import Book, SessionDep

from .schemas import BookCreate, BookUpdate


class BookService:
    async def get_all_books(self, session: SessionDep):
        books = session.exec(select(Book)).all()
        return books

    async def get_book_by_id(self, book_id: str, session: SessionDep):
        book = session.exec(select(Book).where(Book.uid == uuid.UUID(book_id))).first()
        if not book:
            raise HTTPException(
                status_code=404, detail=f"Book with id {book_id} not found"
            )
        return book

    async def create_book(
        self,
        book_data: BookCreate,
        session: SessionDep,
        user_uid: str,
    ):
        book = Book(**book_data.model_dump())
        book.user_uid = uuid.UUID(user_uid)
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

    async def update_book(
        self, book_id: str, book_data: BookUpdate, session: SessionDep
    ):
        book = session.get(Book, uuid.UUID(book_id))
        print("Book", book)
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
