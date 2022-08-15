from dataclasses import dataclass
from enum import Enum
from core.utils import DatetimeWithTZ
from core.entities.match import Match


class CompetitionType(Enum):
    OS = 'OS'
    OD = 'OD'
    COD = 'COD'


@dataclass
class Competition:
    id: int
    competition_type: CompetitionType
    matches: list[Match]
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
