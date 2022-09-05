from typing import Optional
from dataclasses import dataclass, field

from common.entities.player import Player
from common.entities.competition import Competition


@dataclass
class Team:
    id: int = field(init=False)
    competition: Competition
    competition_place: int
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
