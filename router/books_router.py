from fastapi import APIRouter
from fastapi import Query
from fastapi import Body

from models import response_model
from models import book_model
from controllers import BooksController

books_router = APIRouter()


@books_router.get("/", response_model=response_model.BooksResponse)
def get_books(limit: int | None = Query(default=None)):
    print("GET BOOKS")
    books = BooksController.get_books(limit)
    return response_model.BooksResponse(data=books)


@books_router.post("/", response_model=response_model.BookResponse)
def add_book(book: book_model.Book = Body()):
    new_book = BooksController.add_book(book=book)
    return response_model.BookResponse(data=new_book, message="book added")


@books_router.delete("/{book_id}", response_model=response_model.BaseResponse)
def delete_book(book_id: str):
    BooksController.delete_book(book_id=book_id)
    return response_model.BaseResponse(message="book deleted")
