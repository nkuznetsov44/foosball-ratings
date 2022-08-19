from typing import Optional
from decimal import Decimal
from dataclasses import dataclass, field
from sqlalchemy import DateTime, Table, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from common.utils import DatetimeWithTZ
from common.enums import CompetitionType
from core.storage.mapping import mapper_registry
from core.entities.match import Match


@mapper_registry.mapped
@dataclass
class Competition:
    __table__ = Table(
        "competitions",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("tournament_id", Integer, ForeignKey("tournaments.id")),
        Column("competition_type", String(63)),
        Column("evks_importance_coefficient", Numeric),
        Column("match_id", Integer, ForeignKey("matches.id")),
        Column("start_datetime", DateTime(timezone=True)),
        Column("end_datetime", DateTime(timezone=True)),
    )

    __mapper_args__ = {  # type: ignore
        "properties": {
            "matches": relationship("Match"),
        }
    }

    id: Optional[int] = field(init=False)
    competition_type: CompetitionType
    evks_importance_coefficient: Decimal
    matches: list[Match]
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
