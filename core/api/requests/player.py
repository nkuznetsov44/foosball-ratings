from typing import Optional
from dataclasses import dataclass


@dataclass
class PlayerReq:
    first_name: str
    last_name: str
    initial_evks_rating: Optional[int]


@dataclass
class CreatePlayersRequest:
    players: list[PlayerReq]
