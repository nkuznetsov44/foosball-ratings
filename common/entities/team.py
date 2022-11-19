from typing import Optional
from dataclasses import dataclass

from common.entities.player import Player


@dataclass
class Team:
    id: int
    competition_id: int
    competition_place: int
    competition_order: int
    first_player: Player
    second_player: Optional[Player]  # None for singles
    external_id: Optional[int] = None

    @property
    def is_single_player(self) -> bool:
        return self.second_player is None

    @property
    def players(self) -> list[Player]:
        if self.second_player:
            return [self.first_player, self.second_player]
        return [self.first_player]
