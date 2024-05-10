from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy import CheckConstraint, Column
from sqlalchemy.orm import Mapped, mapped_column
from config import settings

from database import Base


class ImageOrm(Base):
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(primary_key=True)
    path = Column(FileType(storage=settings.files.img_storage), nullable=False)
    __table_args__ = (
        CheckConstraint(
            "image_url != ''",
            name="check_image_url",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
        }
