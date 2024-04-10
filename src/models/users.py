from datetime import datetime
from pydantic import EmailStr
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base



class UserOrm(Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[EmailStr] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    is_superuser: Mapped[bool] = mapped_column(nullable=False)
    is_male: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=("TIMEZONE('utc', now())"))

    user_metrics: Mapped["UserMetricsOrm"] = relationship(back_populates="user")

class UserMetricsOrm(Base):
    __tablename__ = "user_metrics"
    height: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    goal: Mapped[str] = mapped_column(nullable=False)
    weight_preference: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["UserOrm"] = relationship(back_populates='user_metrics')
