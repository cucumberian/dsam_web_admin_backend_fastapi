from pydantic import BaseModel
from models import book_model
from typing import Any


class BaseResponse(BaseModel):
    status_code: int | None = None
    success: bool | None = True
    data: Any | None = None
    message: str | None = None


class Response200(BaseResponse):
    status_code: int = 200
    success: bool | None = True
    message: str | None = "Успешно"


class ErrorResponse(BaseResponse):
    status_code: int | None = 500
    success: bool | None = False
    data: Any | None = None
    message: str | None = "Ошибка"


class BooksResponse(BaseResponse):
    data: list[book_model.Book] | None = None


class BookResponse(BaseResponse):
    data: book_model.Book | None = None
