from typing import Optional
from dataclasses import dataclass, field
from sqlalchemy import Table, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from common.enums import City
from core.storage.mapping import mapper_registry
from core.entities.competition import Competition


@mapper_registry.mapped
@dataclass
class Tournament:
    __table__ = Table(
        "tournaments",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("external_id", Integer, nullable=True, unique=True),
        Column("name", String(255)),
        Column("city", Enum(City)),
        Column("url", String(511), nullable=True),
    )

    __mapper_args__ = {  # type: ignore
        "properties": {
            "competitions": relationship(Competition),
        }
    }

    id: int = field(init=False)
    name: str
    city: City
    url: Optional[str]
    competitions: list[Competition] = field(default_factory=list)
    external_id: Optional[int] = None
