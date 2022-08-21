from typing import Optional
from decimal import Decimal
from dataclasses import dataclass, field
from sqlalchemy import (
    DateTime,
    Table,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from common.utils import DatetimeWithTZ
from common.enums import CompetitionType
from core.storage.mapping import mapper_registry
from core.entities.match import Match
from core.entities.team import Team


@mapper_registry.mapped
@dataclass
class Competition:
    __table__ = Table(
        "competitions",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("external_id", Integer, nullable=True),
        Column("tournament_id", Integer, ForeignKey("tournaments.id")),
        Column("competition_type", Enum(CompetitionType)),
        Column("evks_importance_coefficient", Numeric),
        Column("start_datetime", DateTime(timezone=True)),
        Column("end_datetime", DateTime(timezone=True)),
    )

    __table_args__ = (UniqueConstraint("tournament_id", "external_id"),)

    __mapper_args__ = {  # type: ignore
        "properties": {
            "matches": relationship(Match),
            "teams": relationship(Team),
        }
    }

    id: int = field(init=False)
    tournament_id: int = field(init=False)
    competition_type: CompetitionType
    evks_importance_coefficient: Decimal
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
    matches: list[Match]
    teams: list[Team]
    external_id: Optional[int] = None
