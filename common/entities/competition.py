from typing import Optional
from decimal import Decimal
from dataclasses import dataclass

from common.utils import DatetimeWithTZ
from common.entities.enums import CompetitionType
from common.entities.tournament import Tournament


@dataclass
class Competition:
    id: int
    tournament: Tournament
    competition_type: CompetitionType
    evks_importance_coefficient: Decimal
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
    external_id: Optional[int] = None
