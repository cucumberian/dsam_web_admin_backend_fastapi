from .database import MongoDB
from .database import mongodb
from models.book_model import Book
from models.user_model import User
from models.user_model import UserAdd


def get_books(limit: int | None = 10) -> list[Book]:
    books: list[Book] = mongodb.get_books(limit=limit)
    return books


def add_book(book: Book) -> Book:
    result = mongodb.db["books"].insert_one(book.model_dump(by_alias=True))
    book.id = result.inserted_id
    return book


def delete_book(book_id: str) -> int:
    # delete and return deleted count
    result = mongodb.db["books"].delete_one({"_id": book_id})
    return result.deleted_count


def get_users() -> list[User]:
    query = {}
    filter = {"password_hash": 0}
    users = [User(**data) for data in mongodb.db["users"].find(query, filter)]
    print(f"{users =}")
    return users


def add_user(user: UserAdd) -> UserAdd:
    """
    Adds a user to the database
    params:
        user: UserAdd - user to add to database
    returns:
        UserAdd - user added to database
    """
    mongodb.db["users"].insert_one(user.model_dump(by_alias=True))
    return user


def delete_user(user_id: str) -> int:
    """
    Deletes a user from the database
    params:
        user_id: str - id of the user to delete from the database
    returns:
        int - number of documents deleted
    """
    # delete and return deleted count
    result = mongodb.db["users"].delete_one({"_id": user_id})
    return result.deleted_count


def get_book_by_id(book_id: str) -> Book | None:
    book: Book = mongodb.get_book_by_id(book_id=book_id)
    if not book:
        return None
