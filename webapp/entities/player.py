from dataclasses import dataclass
from sqlalchemy import Table, Column, String, Integer, Enum
from common.enums import City
from webapp.storage.mapping import mapper_registry


@mapper_registry.mapped
@dataclass
class Player:
    __table__ = Table(
        "players",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("first_name", String(255)),
        Column("last_name", String(255)),
        Column("city", Enum(City)),
    )

    id: int
    first_name: str
    last_name: str
    city: City
