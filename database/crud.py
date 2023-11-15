from .database import MongoDB

from .pydantic_models import Book
from .pydantic_models import BookToPost
from .pydantic_models import User
from .pydantic_models import UserToPost


def get_books(limit: int | None = 10) -> list[Book]:
    with MongoDB() as db:
        books: list[Book] = db.get_books(limit=limit)
        return books


def create_book(book: BookToPost) -> Book:
    with MongoDB() as db:
        book = db.add_book(book)
        return book


def get_users() -> list[User]:
    with MongoDB() as db:
        users: list[User] = db.get_users()
        return users


def add_user(user: UserToPost) -> User:
    with MongoDB() as db:
        user = db.add_user(user)
        return user
