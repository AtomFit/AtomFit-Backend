from pydantic_settings import BaseSettings
import os

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


class Settings(BaseSettings):
    app_name: str = "FastAPI"
    debug: bool = False
    testing: bool = False
    database_url: str = f"postgresql+async://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PASS}/{DB_NAME}"

settings = Settings()
