from datetime import datetime
from typing import Final

from sqlalchemy import CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, validates
import re

from database import Base

GOAL_OPTIONS: Final = ("lose", "maintain", "gain")


class UserOrm(Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    is_male: Mapped[bool] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    height: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    goal: Mapped[str] = mapped_column(nullable=False)
    weight_preference: Mapped[float] = mapped_column(nullable=False)

    __table_args__ = (
        CheckConstraint(
            goal.in_(list(GOAL_OPTIONS)),
            name="check_goal",
        ),
    )

    @validates("email")
    def validate_email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email
