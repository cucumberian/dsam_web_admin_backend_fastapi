from fastapi import APIRouter

from .books_router import books_router
from .users_router import users_router

index_router = APIRouter()

index_router.include_router(prefix="/books", router=books_router)
index_router.include_router(prefix="/users", router=users_router)
