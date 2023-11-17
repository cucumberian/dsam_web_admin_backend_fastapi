from fastapi import APIRouter

from .books_router import books_router
from .user_router import user_router

index_router = APIRouter()

index_router.include_router(prefix="/books", router=books_router)
index_router.include_router(prefix="/users", router=user_router)
