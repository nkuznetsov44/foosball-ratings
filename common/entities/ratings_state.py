from typing import Optional, Union
from dataclasses import dataclass

from common.entities.enums import EvksPlayerRank, RatingsStateStatus
from common.entities.player import Player
from common.entities.competition import Competition
from common.entities.player_state import PlayerState


_PlayerId = int


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
