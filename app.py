from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import Config
from router import index_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = f"/api/{Config.api_version}"

app.include_router(
    prefix=API_URL,
    router=index_router,
)


def main():
    uvicorn.run(app="app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
