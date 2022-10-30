from dataclasses import dataclass

from common.entities.enums import EvksPlayerRank, RatingType


@dataclass
class PlayerStateResp:
    player_id: int
    player_name: str
    evks_rank: EvksPlayerRank
    rating: int
    is_evks_player_active: bool


@dataclass
class RatingsStateResponse:
    id: int
    rating_type: RatingType
    player_states: list[PlayerStateResp]
