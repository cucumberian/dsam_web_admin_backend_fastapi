from datetime import datetime
from pydantic import BaseModel
from pydantic import Field
from pydantic import BaseConfig
from json.objectid import ObjectId
import utils


class MongoModel(BaseModel):
    class Config(BaseConfig):
        populate_by_name = True
        json_encoders = {
            ObjectId: lambda id: str(id),
            datetime: lambda dt: dt.isoformat(),
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    role: str | None = None


class UserToPost(BaseModel):
    username: str
    password: str
    role: str


class User(MongoModel):
    id: str | None = Field(default=None, alias="_id")
    username: str = Field(...)
    password_hash: str
    role: str

    def verify_hash(self, password: str) -> str | None:
        return utils.verify_password_hash(
            password=password, password_hash=self.password_hash
        )

    def has_role(self, role: str) -> bool:
        """
        Check if user has a specific role

        params: role: role to check (str)
        returns: True if user has the role, False otherwise (bool)
        raises: None
        """
        return role == self.role


class BookToPost(BaseModel):
    title: str = Field(...)
    author: str
    url: str
    date_added: datetime | None = None
    description: str | None = None
    file_ids: list[str] | None = []


class Book(MongoModel):
    id: str | None = Field(default=None, alias="_id")
    title: str = Field(...)
    author: str
    url: str
    date_added: datetime | None = None
    description: str | None = None
    file_ids: list[str] | None = []
