from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class UserRole(Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class User(BaseModel):
    id: str | None = Field(default=None, alias="_id")
    email: EmailStr | None = Field(default=None)
    password_hash: str = Field(exclude=True)
    roles: set[UserRole]
