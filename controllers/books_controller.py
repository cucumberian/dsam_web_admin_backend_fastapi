from fastapi import Depends

from database import pydantic_models
from database import crud

from . import auth_controller


class BooksController:
    @staticmethod
    def get_books(limit: int) -> list[pydantic_models.Book]:
        books = crud.get_books(limit)
        return books

    @staticmethod
    def create_new_book(
        book: pydantic_models.BookToPost,
        user=Depends(auth_controller.get_current_admin),
    ):
        return crud.create_book(book)
