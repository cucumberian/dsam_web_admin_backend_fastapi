from .database import MongoDB
from models.book_model import Book


def get_books(limit: int | None = 10) -> list[Book]:
    with MongoDB() as db:
        books: list[Book] = db.get_books(limit=limit)
        return books

def add_book(book: Book) -> Book:
    with MongoDB() as db:
        result = db.db["books"].insert_one(book.model_dump(by_alias=True))
        book.id = result.inserted_id
        return book

def delete_book(book_id: str) -> int:
    with MongoDB() as db:
        # delete and return deleted count
        result = db.db["books"].delete_one({"_id": book_id})
        return result.deleted_count
