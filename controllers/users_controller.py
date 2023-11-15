from database.pydantic_models import User
from database.pydantic_models import UserToPost
from database import crud


class UserController:
    @staticmethod
    def get_users() -> list[User]:
        users = crud.get_users()
        return users

    @staticmethod
    def add_user(user: UserToPost) -> User:
        added_user = crud.add_user(user)
        return added_user
