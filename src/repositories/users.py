from models.users import UserOrm, UserMetricsOrm
from utils.repositories import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = UserOrm

class UserMetricsRepository(SQLAlchemyRepository):
    model = UserMetricsOrm
