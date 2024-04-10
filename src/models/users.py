from datetime import datetime
from sqlalchemy import ForeignKey, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
import re

from src.database import Base

GOAL_OPTIONS = ["lose", "maintain", "gain"]


class UserOrm(Base):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    user_metrics: Mapped["UserMetricsOrm"] = relationship(back_populates="user")

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email


class UserMetricsOrm(Base):
    __tablename__ = "user_metrics"
    is_male: Mapped[bool] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    height: Mapped[float] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    goal: Mapped[str] = mapped_column(nullable=False)
    weight_preference: Mapped[float] = mapped_column(nullable=False)

    user: Mapped["UserOrm"] = relationship(back_populates='user_metrics')

    __table_args__ = (
        CheckConstraint(
            goal.in_(GOAL_OPTIONS),
            name="check_goal",
        ),
    )
