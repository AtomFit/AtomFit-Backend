from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __table__ = False


    repr_cols_count = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_count:
                cols.append(f"{col}={getattr(self, col)}")

        return f"{self.__class__.__name__}({', '.join(cols)})"


