from typing import Optional, Union
from dataclasses import dataclass

from common.entities.enums import RatingType, EvksPlayerRank, RatingsStateStatus
from common.entities.player import Player
from common.entities.match import Match
from common.entities.competition import Competition


_RatingValue = int
_PlayerId = int


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


@dataclass
class RatingsState:
    """Описывает состояние рейтингов после истории сыгранных категорий."""

    id: int
    previous_state_id: Optional[int]
    last_competition: Optional[Competition]
    player_states: dict[_PlayerId, PlayerState]
    evks_player_ranks: dict[_PlayerId, EvksPlayerRank]
    status: RatingsStateStatus

    # TODO:
    # created: Timestamp
    # updated: Timestamp
    # created_with: jsonb  # save request id

    @property
    def player_states_list(self) -> list[PlayerState]:
        return list(self.player_states.values())

    def __getitem__(self, item: Union[_PlayerId, Player]) -> Optional[PlayerState]:
        if isinstance(item, Player):
            player_id = item.id
            if player_id is None:
                raise KeyError(f"Can't get player state for player with no id {item}")
        elif isinstance(item, _PlayerId):
            player_id = item
        else:
            raise KeyError(f"Incorrect player state key type {type(item)}")
        return self.player_states.get(player_id)
