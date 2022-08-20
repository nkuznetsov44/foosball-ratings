from typing import Optional
from dataclasses import dataclass, field
from sqlalchemy import Table, Column, String, Integer, Enum
from common.enums import City
from core.storage.mapping import mapper_registry


@mapper_registry.mapped
@dataclass
class Player:
    __table__ = Table(
        "players",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("external_id", Integer, nullable=True, unique=True),
        Column("first_name", String(255)),
        Column("last_name", String(255)),
        Column("city", Enum(City)),
    )

    id: int = field(init=False)
    first_name: str
    last_name: str
    city: City
    external_id: Optional[int] = None

    def __hash__(self) -> int:
        assert self.id is not None
        return hash(self.id)
