from .database import MongoDB

from .pydantic_models import Book


def get_books(limit: int | None = 10) -> list[Book]:
    with MongoDB() as db:
        books: list[Book] = [Book(**book) for book in db.get_books(limit=limit)]
        return books
