import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # echo: bool = False
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "rsa.private"
    public_key_path: Path = BASE_DIR / "rsa.public"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    # refresh_token_expire_minutes: int = 60 * 24 * 30
    # access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()

    # db_echo: bool = True


settings = Settings()
