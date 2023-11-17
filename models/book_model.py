import datetime
import random

from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict


class Book(BaseModel):
    """Модель книги"""

    # изначально ид определялся как sha256 хэш от "автора_название"
    # поэтому для создания ид генерируем случайные 256 бит 
    # и преобразуем в строку в 16 формате
    id: str | None = Field(
        alias="_id", default_factory=lambda: f"{random.getrandbits(256):x}"
    )
    title: str = Field(...)
    author: str = Field(...)
    url: str = Field(...)
    date_added: datetime.datetime | None = Field(
        default_factory=lambda: datetime.datetime.utcnow()
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
