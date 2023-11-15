import os


class Config:
    mongo_user = os.environ.get("MONGO_LOGIN")
    mongo_password = os.environ.get("MONGO_PASSWORD")
    mongo_connection_string = f"mongodb+srv://{mongo_user}:{mongo_password}@netheland.6vqpu.mongodb.net/?retryWrites=true&w=majority"
    mongo_db_name = os.environ.get("MONGO_DB_NAME")
