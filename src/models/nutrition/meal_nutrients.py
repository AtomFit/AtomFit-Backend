from datetime import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import relationship, mapped_column, Mapped

from database import Base


class MealNutrientsOrm(Base):
    __tablename__ = "meal_nutrients"
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    proteins: Mapped[int] = mapped_column(nullable=False)
    fats: Mapped[int] = mapped_column(nullable=False)
    carbohydrates: Mapped[int] = mapped_column(nullable=False)
    calories: Mapped[int] = mapped_column(nullable=False)
    fibers: Mapped[int] = mapped_column(nullable=False)
    sugars: Mapped[int] = mapped_column(nullable=False)
    log_date: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    user = relationship("UserOrm")
