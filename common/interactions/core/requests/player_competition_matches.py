from typing import Optional, Sequence
from dataclasses import dataclass

from common.entities.enums import RatingType
from common.entities.player import Player
from common.entities.match import Match, GrandFinalOptions
from common.utils import DatetimeWithTZ


@dataclass
class TeamResp:
    competition_place: int
    competition_order: int
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
    is_forfeit: bool
    grand_final_options: Optional[GrandFinalOptions]
    # sets: list[MatchSetResp]  # FIXME
    # player_state: PlayerStateResp  # FIXME


@dataclass
class PlayerCompetitionMatchesResponse:
    matches: list[MatchResp]

    @classmethod
    def from_matches(
        cls, matches: Sequence[Match]
    ) -> "PlayerCompetitionMatchesResponse":
        # TODO: join Sets and PlayerState
        match_resps: list[MatchResp] = []
        for match in matches:
            match_resps.append(
                MatchResp(
                    id=match.id,
                    first_team=TeamResp(
                        competition_place=match.first_team.competition_place,
                        competition_order=match.first_team.competition_order,
                        first_player=match.first_team.first_player,
                        second_player=match.first_team.second_player,
                    ),
                    second_team=TeamResp(
                        competition_place=match.second_team.competition_place,
                        competition_order=match.second_team.competition_order,
                        first_player=match.second_team.first_player,
                        second_player=match.second_team.second_player,
                    ),
                    start_datetime=match.start_datetime,
                    end_datetime=match.end_datetime,
                    force_qualification=match.force_qualification,
                    is_forfeit=match.is_forfeit,
                    grand_final_options=match.grand_final_options,
                )
            )
        return PlayerCompetitionMatchesResponse(match_resps)
