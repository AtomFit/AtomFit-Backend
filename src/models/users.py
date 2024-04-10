from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class User(Base):
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[EmailStr] = mapped_column(nullable=False, unique=True)