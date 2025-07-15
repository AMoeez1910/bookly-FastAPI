"""Books module exports."""

from .routes import book_router
from .schemas import Book as BookSchema
from .schemas import BookAttributes, BookCreate, BookUpdate
from .service import BookService

__all__ = [
    "BookSchema",
    "BookCreate",
    "BookService",
    "book_router",
    "BookAttributes",
    "BookUpdate",
]
