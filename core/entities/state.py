from enum import Enum
from typing import Optional
from dataclasses import dataclass
from core.entities.player import Player
from core.entities.match import Match
from core.entities.rating import RatingType
from core.entities.competition import Competition


class EvksPlayerRank(Enum):
    BEGINNER = "Beginner"
    NOVICE = "Novice"
    AMATEUR = "Amateur"
    SEMIPRO = "Semipro"
    PRO = "Pro"
    MASTER = "Master"


@dataclass
class PlayerState:
    """Описывает состояние рейтингов игрока после истории сыгранных матчей."""

    id: int
    player: Player
    matches_played: int  # суммарное количество матчей, сыгранное к этому моменту
    last_match: Optional[
        Match
    ]  # optional for players initial state where no matches were played
    ratings: dict[RatingType, int]
    is_evks_rating_active: bool

    @property
    def evks_rating(self) -> Optional[int]:
        return self.ratings.get(RatingType.EVKS)

    @property
    def cumulative_rating(self) -> Optional[int]:
        return self.rating.get(RatingType.CUMULATIVE)

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class RatingsState:
    """Описывает состояние рейтингов после истории сыгранных категорий."""

    id: int
    previous_state_id: int  # начальное состояние указывает само на себя
    player_states: set[PlayerState]
    player_evks_ranks: dict[int, EvksPlayerRank]  # maps player_id -> EvksPlayerRank
    last_competition: Optional[
        Competition
    ]  # optional for initial state where no competition were played

    def lookup_player_state(self, player: Player) -> Optional[PlayerState]:
        return next(
            filter(lambda ps: ps.player.id == player.id, self.player_states), None
        )

    def __hash__(self) -> int:
        return hash(self.id)
