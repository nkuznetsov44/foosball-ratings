from typing import Optional
from dataclasses import dataclass, field
from datetime import date
from sqlalchemy import Date, Table, Column, Integer, String
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
        Column("name", String(255)),
        Column("city", String(63)),
        Column("start_date", Date),
        Column("end_date", Date),
        Column("url", String(511), nullable=True),
    )

    __mapper_args__ = {  # type: ignore
        "properties": {
            "competitions": relationship("Competition"),
        }
    }

    id: Optional[int] = field(init=False)
    name: str
    city: City
    start_date: date
    end_date: date
    url: Optional[str]
    competitions: list[Competition]
