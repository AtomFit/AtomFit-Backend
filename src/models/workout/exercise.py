from sqlalchemy import text, CheckConstraint, Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

from database import Base
from models.images import ImageOrm


class ExerciseOrm(Base):
    __tablename__ = "exercise"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(String(500))
    video_url: Mapped[str]
    image_id = Column(Integer, ForeignKey("image.id", ondelete="SET NULL"))

    image: Mapped["ImageOrm"] = relationship()

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
            "image": self.image.to_dict(),
        }
