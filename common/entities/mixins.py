from sqlalchemy import Table


class TableMixin:
    @classmethod
    def table(cls) -> Table:
        return cls.__table__
