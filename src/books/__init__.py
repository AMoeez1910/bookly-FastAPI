"""Books module exports."""

from .models import Book
from .routes import book_router
from .schemas import Book as BookSchema
from .schemas import BookCreate
from .service import BookService

__all__ = [
    "BookSchema",
    "Book",
    "BookCreate",
    "BookService",
    "book_router",
]
