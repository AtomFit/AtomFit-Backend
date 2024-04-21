from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserGoalNutrientsOrm(Base):
    __tablename__ = "user_goal_nutrients"
    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    proteins: Mapped[int] = mapped_column(nullable=False)
    fats: Mapped[int] = mapped_column(nullable=False)
    carbohydrates: Mapped[int] = mapped_column(nullable=False)
    calories: Mapped[int] = mapped_column(nullable=False)
    fibers: Mapped[int] = mapped_column(nullable=False)
    sugars: Mapped[int] = mapped_column(nullable=False)

    def to_dict_nutrients(self):
        return {
            "proteins": self.proteins,
            "fats": self.fats,
            "carbohydrates": self.carbohydrates,
            "calories": self.calories,
            "fibers": self.fibers,
            "sugars": self.sugars,
        }
