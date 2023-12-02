import pymongo
from .db_config import Config

from models import book_model


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

    def get_books(self, limit: int | None = 10) -> list[book_model.Book]:
        book_list = []
        print("DB GET BOOKS")
        if limit:
            try:
                limit = int(limit)
            except Exception:
                limit = None
        if limit is None:
            book_list = self.db["books"].find()
        else:
            book_list = self.db["books"].find().limit(limit)

        books = []
        for book in book_list:
            try:
                books.append(book_model.Book(**book))
            except Exception:
                print(f"\nERROR in {book}")
        return books

    # def __del__(self) -> None:
    # self.close()
    # print("Database connection closed.")

    def close(self) -> None:
        # self.client.close()
        pass

    def get_users(self):
        users = self.db["users"].find()
        return users


mongodb = MongoDB()
