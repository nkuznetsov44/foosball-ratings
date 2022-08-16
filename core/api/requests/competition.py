from typing import Optional
from dataclasses import dataclass, field
from decimal import Decimal
from marshmallow import fields
from common.utils import DatetimeWithTZ
from core.entities.competition import CompetitionType


@dataclass
class TeamReq:
    first_player_id: int
    second_player_id: Optional[int]  # None for singles


@dataclass
class MatchSetReq:
    first_team_score: int
    second_team_score: int


@dataclass
class MatchReq:
    first_team: TeamReq
    second_team: TeamReq
    sets: list[MatchSetReq]
    force_qualification: Optional[bool]
    start_datetime: DatetimeWithTZ = field(
        metadata=dict(marshmallow_field=fields.DateTime())
    )
    end_datetime: DatetimeWithTZ = field(
        metadata=dict(marshmallow_field=fields.DateTime())
    )


@dataclass
class CreateCompetitionRequest:
    tournament_id: int
    competition_type: CompetitionType
    evks_importance_coefficient: Decimal
    city: str
    matches: list[MatchReq]
