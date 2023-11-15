from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from database import pydantic_models
import exceptions
import controllers.auth_controller as AuthController

token_router = APIRouter()


@token_router.post("/")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> pydantic_models.Token:
    username = form_data.username
    password = form_data.password
    user = AuthController.authenticate_user(
        username=username, password=password
    )
    if user is None:
        raise exceptions.CREDENTIAL_EXCEPTION
    token_data = {
        "sub": user.username,
        "role": user.role,
    }
    token = AuthController.create_access_token(
        token_data=token_data,
    )
    return {"access_token": token, "token_type": "bearer"}
