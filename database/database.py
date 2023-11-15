import pymongo
import datetime
from .db_config import Config
from .pydantic_models import Book
from .pydantic_models import BookToPost
from .pydantic_models import User
from .pydantic_models import UserToPost
import controllers.auth_controller as AuthController


class MongoDB:
    db_name = Config.mongo_db_name
    connection_string = Config.mongo_connection_string

    def __init__(
        self,
        connection_string: str = connection_string,
        db_name: str = db_name,
    ) -> None:
        print("MongoDB connected")
        self.client = pymongo.MongoClient(connection_string)
        self.db = self.client[db_name]

    def __enter__(self) -> "MongoDB":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
        print("Database connection closed.")

    def get_books(self, limit: int | None = 10) -> list[Book]:
        query = {}
        books = []
        print("DB GET BOOKS")
        if limit:
            try:
                limit = int(limit)
            except Exception:
                limit = None
        if limit is None:
            books = self.db["books"].find(
                query,
            )
        else:
            books = self.db["books"].find(query).limit(limit)
        # print(f"{books = }")
        book_list = [book for book in books]
        books = []
        for book in book_list:
            try:
                books.append(Book(**book))
            except Exception:
                print(f"ERROR in {book}")
        # books = [Book(**book) for book in book_list]
        return books

    def add_book(self, book: BookToPost) -> Book:
        """
        Add book to MongoDB
        params: book: book to add (BookToPost)
        return: added_book: Book (pydantic model)
        """
        date_added = datetime.datetime.now()
        book.date_added = date_added
        id = self.db["books"].insert_one(book.dict()).inserted_id
        new_book = Book(**book.dict())
        new_book.id = str(id)
        new_book.date_added = date_added
        print(f"{new_book = }")
        return new_book

    def get_users(self) -> list[User]:
        query = {}
        result = self.db["users"].find(query)
        users = list(result)
        print(f"DB {users = }")
        user_list = [User(**user) for user in users]
        print(f"{user_list = }")
        return user_list

    def get_user(self, user_id: str) -> User:
        query = {"id": user_id}
        user: User = self.db["users"].find_one(query)
        return user

    def add_user(self, user: UserToPost) -> User:
        password_hash = AuthController.get_password_hash(user.password)
        add_data = {
            "username": user.username,
            "role": user.role,
            "password_hash": password_hash,
        }
        print(f"{add_data = }")
        user_id = self.db["users"].insert_one(add_data).inserted_id
        add_data["_id"] = str(user_id)
        new_user = User(**add_data)
        print(f"{new_user = }")
        return new_user

    def __del__(self) -> None:
        self.close()
        print("Database connection closed.")

    def close(self) -> None:
        self.client.close()
