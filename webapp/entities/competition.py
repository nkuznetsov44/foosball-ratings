from typing import Optional
from decimal import Decimal
from dataclasses import dataclass
from sqlalchemy import (
    DateTime,
    Table,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Enum,
    String,
)
from sqlalchemy.orm import relationship
from common.utils import DatetimeWithTZ
from common.enums import CompetitionType, City
from webapp.storage.mapping import mapper_registry


@mapper_registry.mapped
@dataclass
class Competition:
    __table__ = Table(
        "competitions",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("tournament_id", Integer, ForeignKey("tournaments.id")),
        Column("competition_type", Enum(CompetitionType)),
        Column("evks_importance_coefficient", Numeric),
        Column("start_datetime", DateTime(timezone=True)),
        Column("end_datetime", DateTime(timezone=True)),
    )

    id: int
    tournament: "Tournament"
    competition_type: CompetitionType
    evks_importance_coefficient: Decimal
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ


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

    __mapper_args__ = {
        "properties": {
            "competitions": relationship(Competition, backref="tournament"),
        }
    }

    id: int
    name: str
    city: City
    url: Optional[str]
    competitions: list[Competition]
    external_id: Optional[int] = None
