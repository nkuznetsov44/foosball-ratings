from enum import Enum
from typing import Optional
from dataclasses import dataclass
from core.entities.player import Player
from core.entities.match import Match
from core.entities.rating import RatingType
from core.entities.competition import Competition


class EvksPlayerRank(Enum):
    BEGINNER = 'Beginner'
    NOVICE = 'Novice'
    AMATEUR = 'Amateur'
    SEMIPRO = 'Semipro'
    PRO = 'Pro'
    MASTER = 'Master'


@dataclass
class PlayerState:
    """Описывает состояние рейтингов игрока после истории сыгранных матчей."""
    id: int
    player: Player
    last_match: Optional[Match]  # optional for players initial state where no matches were played
    ratings: dict[RatingType, int]

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class RatingsState:
    """Описывает состояние рейтингов после истории сыгранных категорий."""
    id: Optional[int]
    player_states: set[PlayerState]
    player_evks_ranks: dict[int, EvksPlayerRank]  # maps player_id -> EvksPlayerRank
    last_competition_id: Optional[Competition]  # optional for initial state where no competition were played

    def lookup_player_state(self, player: Player) -> Optional[PlayerState]:
        return next(filter(lambda ps: ps.player.id == player.id, self.player_states), None)

    def __hash__(self) -> int:
        return hash(self.id)
