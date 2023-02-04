from typing import Collection, Iterable, Optional, Union, Iterator
from dataclasses import dataclass

from common.entities.enums import RatingsStateStatus
from common.entities.player import Player
from common.entities.player_state import PlayerState


class PlayerStateSet(Collection[PlayerState]):
    def __init__(self, collection: Optional[Collection[PlayerState]] = None) -> None:
        self._dct: dict[int, PlayerState] = {}
        self._st: set[PlayerState] = set()
        if collection:
            self._st = set(collection)
            for player_state in collection:
                self._dct[player_state.player.id] = player_state

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
        return self._dct.get(player_id)

    def __len__(self) -> int:
        return len(self._dct)

    def __contains__(self, __o: object) -> bool:
        if not isinstance(__o, PlayerState):
            raise ValueError
        return __o in self._st

    def __iter__(self) -> Iterator[PlayerState]:
        for player_state in self._st:
            yield player_state

    def update(self, *player_states: Iterable[PlayerState]) -> None:
        for player_state in player_states:
            self.add(player_state)

    def add(self, player_state: PlayerState) -> None:
        old_ps = self.get(player_state.player.id)
        self._st.discard(old_ps)
        self._dct[player_state.player.id] = player_state
        self._st.add(player_state)

    def remove(self, player_state: PlayerState) -> None:
        self._dct.pop(player_state.player.id)
        self._st.discard(player_state)

    def discard(self, player_state: PlayerState) -> None:
        self._dct.pop(player_state.player.id, None)
        self._st.discard(player_state)

    def clear(self) -> None:
        self._dct = {}
        self._st = set()

    def to_list(self) -> list[PlayerState]:
        return list(self._st)

    def __repr__(self) -> str:
        return repr(list(self._st))


@dataclass
class RatingsState:
    """Описывает состояние рейтингов после истории сыгранных категорий."""

    id: int
    previous_state_id: Optional[int]
    last_competition_id: Optional[int]
    player_states: PlayerStateSet
    status: RatingsStateStatus

    # TODO:
    # created: Timestamp
    # updated: Timestamp
    # created_with: jsonb  # save request id
