import time
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from database import pydantic_models
import exceptions
import client
from config import Config


API_URL = f"/api/{Config.api_version}"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=API_URL + "/token/")


def authenticate_user(
    username: str, password: str
) -> pydantic_models.User | None:
    """check user by username and password"""
    user = get_user(username)
    if user is None:
        raise exceptions.CREDENTIAL_EXCEPTION
    is_valid_password = verify_password(
        password=password,
        password_hash=user.password_hash,
    )
    if not is_valid_password:
        raise exceptions.CREDENTIAL_EXCEPTION
    return user


def create_access_token(
    token_data: dict[str:str],
    expires_delta: int = Config.jwt_token_expires_seconds,
):
    """
    Create JWT-string

    params: token_data: data to encode in token (dict)
            expires_delta: time to live (int)
    returns: token (str)
    raises: None
    """
    to_encode = token_data.copy()
    expire = int(time.time()) + expires_delta
    to_encode.update({"exp": str(expire)})
    try:
        token = jwt.encode(
            claims=to_encode,
            key=Config.jwt_secret,
            algorithm=Config.jwt_algorithm,
        )
        return token
    except JWTError:
        return None


def get_password_hash(password: str) -> str | None:
    """
    Hashes a password using the CryptContext

    params: password: password to be hashed (str)
    returns: hashed password (str)
    raises: None
    """
    try:
        pwd_context = CryptContext(
            schemes=Config.crypt_schemes, deprecated="auto"
        )
        password_hash = pwd_context.hash(password)
        return password_hash
    except Exception:
        return None


def verify_password(password: str, password_hash: str) -> bool | None:
    """
    Verifies a password hash using the CryptContext

    params: password: password to be hashed (str)
            password_hash: hashed password (str)
    returns: True if password is correct, False otherwise (bool)
    raises: None
    """
    pwd_context = CryptContext(schemes=Config.crypt_schemes, deprecated="auto")
    try:
        status = pwd_context.verify(secret=password, hash=password_hash)
        return status
    except Exception:
        return None


def get_user(username: str) -> pydantic_models.User | None:
    """Return user by username"""
    if username is None:
        return None
    users = client.users
    for user in users:
        if user.get("username") == username:
            return pydantic_models.User(**user)
    return None


def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> pydantic_models.User | None:
    """Возвращает по токену пользователя, если токен валиден.
    Если токен не валиден поднимет исключение HTTPException.

    params: token: строка, содержащая токен (str)
    returns: pydantic_models.User
    raises: CREDENTIAL_EXCEPTION,
            TOKEN_EXPIRED_EXCEPTION,
            FORBIDDEN_EXCEPTION
    """
    try:
        payload = jwt.decode(
            token=token,
            key=Config.jwt_secret,
            algorithms=[Config.jwt_algorithm],
        )
        username = payload.get("sub")
        if username is None:
            raise exceptions.CREDENTIAL_EXCEPTION
        role = payload.get("role")
        if role is None:
            raise exceptions.CREDENTIAL_EXCEPTION

        try:
            exp = int(payload.get("exp"))
            if exp < time.time():
                print("TOKEN EXPIRED")
                raise exceptions.TOKEN_EXPIRED_EXCEPTION
        except TypeError:
            raise exceptions.CREDENTIAL_EXCEPTION

    except JWTError:
        raise exceptions.CREDENTIAL_EXCEPTION

    user = get_user(username)
    if user is None:
        raise exceptions.CREDENTIAL_EXCEPTION
    return user


def get_current_admin(
    user: pydantic_models.User = Depends(get_current_user),
) -> pydantic_models.User:
    if user.has_role("admin"):
        return user
    raise exceptions.FORBIDDEN_EXCEPTION

    
