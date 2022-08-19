from dataclasses import dataclass, field
from sqlalchemy import Table, Column, String, Integer
from core.storage.mapping import mapper_registry


@mapper_registry.mapped
@dataclass
class Player:
    __table__ = Table(
        "players",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("first_name", String(255)),
        Column("last_name", String(255)),
    )

    id: int = field(init=False)
    first_name: str
    last_name: str

    def __hash__(self) -> int:
        return hash(self.id)
