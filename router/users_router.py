from fastapi import APIRouter
from fastapi import Depends
from fastapi import Body
import controllers.auth_controller as AuthController
from controllers.users_controller import UserController
from database import pydantic_models

users_router = APIRouter()


@users_router.get("/")
def get_users():
    users: list[pydantic_models.User] = UserController.get_users()
    return users


@users_router.post("/")
def add_user(
    user: pydantic_models.UserToPost = Body(),
):
    print(f"router add {user = }")
    user = UserController.add_user(user)
    return {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        }
