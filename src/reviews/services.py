import uuid

from fastapi import HTTPException
from sqlmodel import select

from src.db import Book, Reviews, SessionDep

from .schemas import ReviewCreate


class ReviewService:
    async def create_review(
        self,
        book_id: str,
        review_data: ReviewCreate,
        session: SessionDep,
        user_uid: str,
    ):
        review = Reviews(**review_data.model_dump())
        book = session.exec(select(Book).where(Book.uid == uuid.UUID(book_id))).first()

        if not book:
            raise HTTPException(
                status_code=404, detail=f"Book with id {book_id} not found"
            )
        review.book_uid = uuid.UUID(book_id)
        review.user_uid = uuid.UUID(user_uid)
        review.uid = uuid.uuid4()
        print("------------------Review-------------------\n", review)
        session.add(review)
        session.commit()
        session.refresh(review)
        return review
