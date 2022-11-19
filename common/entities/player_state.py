from typing import Optional
from dataclasses import dataclass

from common.entities.enums import EvksPlayerRank, RatingType
from common.entities.player import Player


_RatingValue = int


@dataclass
class PlayerState:
    """Описывает состояние рейтингов игрока после истории сыгранных матчей."""

    id: int
    previous_state_id: Optional[int]
    player: Player
    matches_played: int
    matches_won: int
    last_match_id: Optional[int]
    ratings: dict[RatingType, _RatingValue]
    evks_rank: EvksPlayerRank
    is_evks_rating_active: bool

    # TODO:
    # created: Timestamp
    # updated: Timestamp
    # created_with: jsonb  # save request id

    @property
    def evks_rating(self) -> Optional[int]:
        return self.ratings.get(RatingType.EVKS)

    @evks_rating.setter
    def evks_rating(self, evks_rating: int) -> Optional[int]:
        self.ratings[RatingType.EVKS] = evks_rating

    @property
    def cumulative_rating(self) -> Optional[int]:
        return self.ratings.get(RatingType.CUMULATIVE)

    @cumulative_rating.setter
    def cumulative_rating(self, cumulative_rating: int) -> Optional[int]:
        self.ratings[RatingType.CUMULATIVE] = cumulative_rating

    def __hash__(self) -> int:
        assert self.id is not None, "Can't hash PlayerState with no id"
        return hash(self.id)
