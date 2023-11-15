from database.database import db
from pydantic_models import Book


books: list[Book] = [Book(**book) for book in db.get_books()]

print(f"{books = }")
# 