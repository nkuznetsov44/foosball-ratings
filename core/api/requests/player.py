from typing import Optional
from dataclasses import dataclass


@dataclass
class PlayerReq:
    first_name: str
    last_name: str
    initial_evks_rating: Optional[int]
    initial_matches_played: Optional[int]
    initial_matches_won: Optional[int]


@dataclass
class CreatePlayersRequest:
    players: list[PlayerReq]
