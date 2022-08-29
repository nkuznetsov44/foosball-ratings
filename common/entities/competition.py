from typing import Optional
from decimal import Decimal
from dataclasses import dataclass, field

from common.utils import DatetimeWithTZ
from common.entities.enums import CompetitionType
from common.entities.match import Match
from common.entities.team import Team


@dataclass
class Competition:
    id: int = field(init=False)
    tournament_id: int = field(init=False)
    competition_type: CompetitionType
    evks_importance_coefficient: Decimal
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
    matches: list[Match]
    teams: list[Team]
    external_id: Optional[int] = None
