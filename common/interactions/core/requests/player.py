from dataclasses import dataclass
from typing import Optional

from common.entities.enums import City


@dataclass
class PlayerRequest:
    first_name: str
    last_name: str
    city: City
    is_foreigner: bool
    external_id: Optional[int] = None
    initial_evks_rating: Optional[int] = None
    initial_cumulative_rating: Optional[int] = None
    initial_matches_played: Optional[int] = None
    initial_matches_won: Optional[int] = None
    is_evks_rating_active: Optional[bool] = None


@dataclass
class CreatePlayersRequest:
    players: list[PlayerRequest]
