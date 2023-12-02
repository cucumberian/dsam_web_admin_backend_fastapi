from models.user_model import User
from models.user_model import UserAdd
from models.user_model import UserRegister
from models import response_model
from database import crud
from passlib.context import CryptContext
from config import Config


class UserController:
    @staticmethod
    def get_users() -> list[User]:
        users = crud.get_users()
        return users

    @staticmethod
    def register_user(user: UserRegister) -> UserAdd:
        """
        Calculates and hashes the password
        and then registers a new user.
        :param user: UserRegister
        :return: UserAdd
        """
        print(f"{user = }")
        pwd_context = CryptContext(
            schemes=Config.crypt_schemes, deprecated="auto"
        )
        password_hash = pwd_context.hash(user.password)
        print(f"{password_hash = }")
        # create new user with hash and post it to database
        new_user = UserAdd(
            login=user.login,
            email=user.email,
            password_hash=password_hash,
            roles=["user"]
        )
        print(f"{new_user = }")
        added_user = crud.add_user(new_user)
        return added_user
