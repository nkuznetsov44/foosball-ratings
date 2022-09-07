from typing import Optional
from dataclasses import dataclass

from common.entities.enums import RatingType
from common.entities.player import Player
from common.entities.match import Match


_RatingValue = int


@dataclass
class PlayerState:
    """Описывает состояние рейтингов игрока после истории сыгранных матчей."""

    id: int
    previous_state_id: Optional[int]
    player: Player
    matches_played: int
    matches_won: int
    last_match: Optional[Match]
    ratings: dict[RatingType, _RatingValue]
    is_evks_rating_active: bool

    # TODO:
    # created: Timestamp
    # updated: Timestamp
    # created_with: jsonb  # save request id

    @property
    def evks_rating(self) -> Optional[int]:
        return self.ratings.get(RatingType.EVKS)

    @property
    def cumulative_rating(self) -> Optional[int]:
        return self.ratings.get(RatingType.CUMULATIVE)

    def __hash__(self) -> int:
        assert self.id is not None, "Can't hash PlayerState with no id"
        return hash(self.id)
