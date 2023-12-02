from fastapi import APIRouter

from controllers.users_controller import UserController
from models.user_model import User
from models.user_model import UserRegister
from models import response_model

users_router = APIRouter()


@users_router.get("/", response_model=response_model.BaseResponse)
def get_users():
    try:
        users: list[User] = UserController.get_users()
        return response_model.Response200(
            data=users, message="Список пользователей"
        )
    except Exception as e:
        return response_model.ErrorResponse(status_code=500, message=str(e))


@users_router.post("/", response_model=response_model.BaseResponse)
def add_user(user_to_register: UserRegister):
    try:
        new_user = UserController.register_user(user=user_to_register)
        return response_model.BaseResponse(
            message="user added", data=User(**new_user.model_dump())
        )

    except Exception as e:
        print(e)
        return response_model.ErrorResponse(status_code=500, message=str(e))
