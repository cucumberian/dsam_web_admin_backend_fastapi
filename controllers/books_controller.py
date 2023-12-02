import random
from models import book_model
from database import crud
import exceptions


class BooksController:
    @staticmethod
    def get_books(limit: int) -> list[book_model.Book]:
        books = crud.get_books(limit)
        return books

    @staticmethod
    def add_book(book: book_model.Book) -> book_model.Book:
        # book id generation in case user has send it
        book.id = f"{random.getrandbits(256):x}"
        new_book = crud.add_book(book)
        return new_book

    @staticmethod
    def delete_book(book_id: str) -> str:
        deleted_count = crud.delete_book(book_id)
        if deleted_count == 0:
            raise exceptions.BOOK_NOT_FOUND_EXCEPTION 
        return deleted_count

# UserWarning: Pydantic serializer warnings:
#  Expected `str` but got `ObjectId` - serialized value may not be as expected
#  return self.__pydantic_serializer__.to_python(
#  Как исправить?

