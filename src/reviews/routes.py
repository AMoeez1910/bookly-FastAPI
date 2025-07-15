from fastapi import APIRouter, Depends

from src.auth import AccessTokenBearer
from src.db import SessionDep

from .schemas import ReviewAttributes, ReviewCreate
from .services import ReviewService

review_router = APIRouter()
access_token_bearer = AccessTokenBearer()
review_service = ReviewService()


@review_router.post("/review/{book_id}", response_model=ReviewAttributes)
async def create_review(
    book_id: str,
    review_data: ReviewCreate,
    session: SessionDep,
    token_details: dict = Depends(access_token_bearer),
):
    user_uid = token_details["user"]["uid"]
    return await review_service.create_review(
        book_id=book_id,
        review_data=review_data,
        session=session,
        user_uid=user_uid,
    )
