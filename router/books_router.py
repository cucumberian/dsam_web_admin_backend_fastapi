from fastapi import APIRouter
from fastapi import Query
from fastapi import Body

from database import pydantic_models
from controllers import BooksController

books_router = APIRouter()


@books_router.get("/")
def get_books(
    limit: int | None = Query(default=None)
) -> list[pydantic_models.Book]:
    print("GET BOOKS")
    books: list[pydantic_models.Book] = BooksController.get_books(limit)
    return books


@books_router.post("/", status_code=201)
def create_new_book(
    book: pydantic_models.BookToPost = Body(),
):
    added_book = BooksController.create_new_book(book)
    print(f"{added_book.dict() = }")
    return added_book.dict()
