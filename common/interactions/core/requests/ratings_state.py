from typing import Optional
from dataclasses import dataclass

from common.entities.enums import (
    City,
    CompetitionType,
    RatingType,
    RatingsStateStatus,
    EvksPlayerRank,
)
from common.entities.player import Player
from common.entities.ratings_state import RatingsState


@dataclass
class TournamentResp:
    id: int
    external_id: Optional[int]
    name: str
    city: City
    url: Optional[str]


@dataclass
class CompetitionResp:
    id: int
    external_id: Optional[int]
    tournament: TournamentResp
    competition_type: CompetitionType


@dataclass
class PlayerStateResp:
    player: Player
    matches_played: int
    matches_won: int
    ratings: dict[RatingType, int]
    evks_rank: EvksPlayerRank
    is_evks_rating_active: bool


@dataclass
class RatingsStateResponse:
    id: int
    last_competition: Optional[CompetitionResp]
    player_states: list[PlayerStateResp]
    status: RatingsStateStatus

    @staticmethod
    def from_ratings_state(ratings_state: RatingsState) -> "RatingsStateResponse":
        last_competition = None
        if ratings_state.last_competition:
            last_competition = CompetitionResp(
                id=ratings_state.last_competition.id,
                external_id=ratings_state.last_competition.external_id,
                tournament=TournamentResp(
                    id=ratings_state.last_competition.tournament.id,
                    external_id=ratings_state.last_competition.tournament.external_id,
                    name=ratings_state.last_competition.tournament.name,
                    city=ratings_state.last_competition.tournament.city,
                    url=ratings_state.last_competition.tournament.url,
                ),
                competition_type=ratings_state.last_competition.competition_type,
            )
        return RatingsStateResponse(
            id=ratings_state.id,
            last_competition=last_competition,
            player_states=[
                PlayerStateResp(
                    player=player_state.player,
                    matches_played=player_state.matches_played,
                    matches_won=player_state.matches_won,
                    ratings=player_state.ratings,
                    evks_rank=player_state.evks_rank,
                    is_evks_rating_active=player_state.is_evks_rating_active,
                )
                for player_state in ratings_state.player_states
            ],
            status=ratings_state.status,
        )
