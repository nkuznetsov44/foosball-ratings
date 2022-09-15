from typing import Collection, Iterable, Optional, Union, Iterator
from dataclasses import dataclass

from common.entities.enums import RatingsStateStatus
from common.entities.player import Player
from common.entities.competition import Competition
from common.entities.player_state import PlayerState


class PlayerStateSet(Collection):
    def __init__(self, collection: Optional[Collection[PlayerState]] = None) -> None:
        self._data: dict[int, PlayerState] = {}
        if collection:
            for player_state in collection:
                self._data[player_state.player.id] = player_state

    def __getitem__(self, item: Union[Player, int]) -> PlayerState:
        player_state = self.get(item)
        if not player_state:
            raise KeyError(f"{item}")
        return player_state

    def get(self, item: Union[Player, int]) -> Optional[PlayerState]:
        if isinstance(item, Player):
            player_id = item.id
            if player_id is None:
                raise KeyError(f"Can't get player state for player with no id {item}")
        elif isinstance(item, int):
            player_id = item
        else:
            raise KeyError(f"Incorrect player state key type {type(item)}")
        return self._data.get(player_id)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, __o: object) -> bool:
        return __o in self._data.values()

    def __iter__(self) -> Iterator[PlayerState]:
        for player_state in self._data.values():
            yield player_state

    def update(self, *player_states: Iterable[PlayerState]) -> None:
        for player_state in player_states:
            self.add(player_state)

    def add(self, player_state: PlayerState) -> None:
        self._data[player_state.player.id] = player_state

    def remove(self, player_state: PlayerState) -> None:
        self._data.pop(player_state.player.id)

    def discard(self, player_state: PlayerState) -> None:
        self._data.pop(player_state.player.id, None)

    def clear(self) -> None:
        self._data = {}

    def to_list(self) -> list[PlayerState]:
        return list(self._data.values())


@dataclass
class RatingsState:
    """Описывает состояние рейтингов после истории сыгранных категорий."""

    id: int
    previous_state_id: Optional[int]
    last_competition: Optional[Competition]
    player_states: PlayerStateSet
    status: RatingsStateStatus

    # TODO:
    # created: Timestamp
    # updated: Timestamp
    # created_with: jsonb  # save request id
