from pydantic import BaseModel
from models import book_model
from typing import Any


class BaseResponse(BaseModel):
    success: bool | None = True
    data: Any | None = None
    message: str | None = None


class BooksResponse(BaseResponse):
    data: list[book_model.Book] | None = None


class BookResponse(BaseResponse):
    data: book_model.Book | None = None
