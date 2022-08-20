from typing import Optional
from dataclasses import dataclass
from common.enums import City


@dataclass
class PlayerReq:
    first_name: str
    last_name: str
    city: City
    initial_evks_rating: Optional[int]
    initial_cumulative_rating: Optional[int]
    initial_matches_played: Optional[int]
    initial_matches_won: Optional[int]
    is_evks_rating_active: Optional[bool]


@dataclass
class CreatePlayersRequest:
    players: list[PlayerReq]
