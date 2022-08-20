from typing import Optional
from dataclasses import dataclass, field
from decimal import Decimal
from marshmallow import fields
from common.utils import DatetimeWithTZ
from common.enums import CompetitionType, City


@dataclass
class TeamReq:
    external_id: Optional[int]
    first_player_id: int
    second_player_id: Optional[int]  # None for singles


@dataclass
class MatchSetReq:
    external_id: Optional[int]
    order: int
    first_team_score: int
    second_team_score: int


@dataclass
class MatchReq:
    external_id: Optional[int]
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
class CompetitionReq:
    external_id: Optional[int]
    competition_type: CompetitionType
    start_datetime: DatetimeWithTZ = field(
        metadata=dict(marshmallow_field=fields.DateTime())
    )
    end_datetime: DatetimeWithTZ = field(
        metadata=dict(marshmallow_field=fields.DateTime())
    )
    matches: list[MatchReq]


@dataclass
class CreateTournamentRequest:
    external_id: Optional[int]
    city: City
    name: str
    evks_importance_coefficient: Decimal
    url: Optional[str]
    competitions: list[CompetitionReq]
