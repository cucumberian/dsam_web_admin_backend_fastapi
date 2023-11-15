from fastapi import APIRouter
from fastapi import Depends

from .books_router import books_router
from .users_router import users_router
from .token import token_router
from database import pydantic_models
import controllers.auth_controller as AuthController

index_router = APIRouter()

index_router.include_router(prefix="/books", router=books_router)
index_router.include_router(prefix="/token", router=token_router)
index_router.include_router(prefix="/users", router=users_router)

@index_router.get(
    path="/admin/",
    response_model=pydantic_models.User,
    status_code=200,
)
def get_admin(
    user: pydantic_models.User = Depends(AuthController.get_current_admin)
) -> pydantic_models.User:
    return user
