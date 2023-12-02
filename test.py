from database.database import mongodb
from models.user_model import User
from database import crud

def get_users() -> list[User]:
        users = list(mongodb.db.users.find())
        return users

users = get_users()
print(users)