from models.images import ImageOrm
from utils.repositories import SQLAlchemyRepository


class ImagesRepository(SQLAlchemyRepository):
    model = ImageOrm
