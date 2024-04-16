import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

load_dotenv()


PRIVATE_KEY_PATH: Path = BASE_DIR / "rsa.private"
PUBLIC_KEY_PATH: Path = BASE_DIR / "rsa.public"
STAGE: Final[str] = os.getenv("STAGE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


def get_public_key(stage) -> str:
    if stage == "dev":
        return PUBLIC_KEY_PATH.read_text()
    elif stage == "prod":
        return os.getenv("PUBLIC_KEY")
    else:
        raise Exception(f"Invalid stage. Stage must be either 'dev' or 'prod'.{stage}")


def get_private_key(stage) -> str:
    if stage == "dev":
        return PRIVATE_KEY_PATH.read_text()
    elif stage == "prod":
        return os.getenv("PRIVATE_KEY")
    else:
        Exception(f"Invalid stage. Stage must be either 'dev' or 'prod'.{stage}")


class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # echo: bool = False
    echo: bool = True


class AuthJWT(BaseModel):
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30
    private_key: str = get_private_key(STAGE)
    public_key: str = get_public_key(STAGE)
    # refresh_token_expire_minutes: int = 60 * 24 * 30
    # access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    stage: Final[str] = STAGE
    auth_jwt: AuthJWT = AuthJWT()

    # db_echo: bool = True


settings = Settings()
