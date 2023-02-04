from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from marshmallow import fields

from common.entities.competition import Competition
from common.entities.enums import CompetitionType
from common.entities.match import GrandFinalOptions
from common.utils import DatetimeWithTZ


@dataclass
class CompetitionTeam:
    external_id: int
    competition_place: int
    competition_order: int
    first_player_id: int
    second_player_id: Optional[int]  # None for singles


@dataclass
class CompetitionMatchSet:
    external_id: Optional[int]
    order: int
    first_team_score: int
    second_team_score: int


@dataclass
class CompetitionMatch:
    external_id: Optional[int]
    first_team_external_id: int
    second_team_external_id: int
    order: int
    sets: list[CompetitionMatchSet]
    force_qualification: Optional[bool]
    grand_final_options: Optional[GrandFinalOptions]
    start_datetime: DatetimeWithTZ = field(
        metadata=dict(marshmallow_field=fields.DateTime())
    )
    end_datetime: DatetimeWithTZ = field(
        metadata=dict(marshmallow_field=fields.DateTime())
    )
    is_forfeit: Optional[bool] = False


@dataclass
class CreateCompetitionRequest:
    tournament_id: int
    external_id: Optional[int]
    competition_type: CompetitionType
    order: int
    evks_importance: Decimal
    cumulative_coefficient: Decimal
    start_datetime: DatetimeWithTZ = field(
        metadata=dict(marshmallow_field=fields.DateTime())
    )
    end_datetime: DatetimeWithTZ = field(
        metadata=dict(marshmallow_field=fields.DateTime())
    )
    matches: list[CompetitionMatch]
    teams: list[CompetitionTeam]
