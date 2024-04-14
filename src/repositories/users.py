from models.users import UserOrm
from utils.repositories import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = UserOrm


