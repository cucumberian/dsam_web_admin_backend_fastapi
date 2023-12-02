from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import BaseConfig
from datetime import datetime
from typing import Literal
from bson import ObjectId


class UserField:
    Login = Field(min_length=3, max_length=50)
    Email = Field()
    Password = Field(min_length=8, max_length=50)
    DateAdded = Field(default_factory=datetime.utcnow)


class UserRole(Enum):
    admin = "admin"
    manager = "manager"
    user = "user"


class MongoModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        # extra = "forbid"
        # json_loads = str.lower
        # json_dumps = str.lower
        # orm_mode = True
        # arbitrary_types_allowed = True
        # type_encoders = {
        #     ObjectId: lambda oid: str(oid),
        #     datetime: lambda dt: dt.isoformat(),
        #     UserRole: lambda role: role.value,
        #     Enum: lambda e: e.value,
        #     bool: lambda b: "true" if b else "false",
        #     int: lambda i: str(i),
        #     float: lambda f: str(f),
        #     str: lambda s: s,
        # }
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
        }


class User(MongoModel):
    login: str = UserField.Login
    email: EmailStr = UserField.Email
    roles: list[Literal["user", "manager", "admin"]]
    date_added: datetime | None = UserField.DateAdded


class UserAdd(User):
    password_hash: str = Field()


class UserRegister(BaseModel):
    login: str = UserField.Login
    email: EmailStr = UserField.Email
    password: str = UserField.Password
