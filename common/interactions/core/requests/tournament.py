from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from marshmallow import fields

from common.entities.enums import City, CompetitionType
from common.utils import DatetimeWithTZ


@dataclass
class TeamReq:
    external_id: int
    competition_place: int
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
    first_team_external_id: int
    second_team_external_id: int
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
    teams: list[TeamReq]


@dataclass
class CreateTournamentRequest:
    external_id: Optional[int]
    city: City
    name: str
    evks_importance: Decimal
    url: Optional[str]
    competitions: list[CompetitionReq]
