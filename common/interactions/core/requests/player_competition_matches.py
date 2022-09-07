from typing import Optional
from dataclasses import dataclass

from common.entities.enums import RatingType
from common.entities.player import Player
from common.utils import DatetimeWithTZ


@dataclass
class TeamResp:
    competition_place: int
    first_player: Player
    second_player: Optional[Player]


@dataclass
class PlayerStateResp:
    matches_played: int
    matches_won: int
    ratings: dict[RatingType, int]
    is_evks_rating_active: bool


@dataclass
class MatchSetResp:
    order: int
    first_team_score: int
    second_team_score: int


@dataclass
class MatchResp:
    id: int
    first_team: TeamResp
    second_team: TeamResp
    start_datetime: DatetimeWithTZ
    end_datetime: DatetimeWithTZ
    force_qualification: Optional[bool]
    # sets: list[MatchSetResp]  # FIXME
    # player_state: PlayerStateResp  # FIXME


@dataclass
class PlayerCompetitionMatchesResponse:
    matches: list[MatchResp]
