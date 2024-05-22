from enum import Enum

from sqlalchemy import text, CheckConstraint, Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from schemas.workout.exercises import MuscleGroups


class ExerciseOrm(Base):
    __tablename__ = "exercise"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(String(500))

    video_url: Mapped[str]

    muscle_groups = Column(Enum(MuscleGroups))

    __table_args__ = (
        CheckConstraint(
            text("video_url != ''"),
            name="check_video_url",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "video_url": self.video_url,
        }
