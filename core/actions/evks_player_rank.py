from typing import Sequence
from common.entities.player_state import PlayerState
from common.entities.enums import EvksPlayerRank
from common.entities.player_state import PlayerState
from core.actions.abstract_action import AbstractAction


_PlayerId = int


class CalculateEvksPlayerRanksAction(AbstractAction[dict[_PlayerId, PlayerState]]):
    def __init__(self, player_states: dict[_PlayerId, PlayerState]) -> None:
        self.player_states = player_states

    async def handle(self) -> dict[_PlayerId, PlayerState]:
        for player_state in self.player_states.values():
            player_state.evks_rank = self._calc_evks_player_rank(player_state)
        return self.player_states

    def _calc_evks_player_rank(self, player_state: PlayerState) -> EvksPlayerRank:
        # TODO: реализовать правильную логику переходов

        if player_state.evks_rating <= 1100:
            return EvksPlayerRank.BEGINNER
        elif 1100 < player_state.evks_rating <= 1200:
            return EvksPlayerRank.NOVICE
        elif 1200 < player_state.evks_rating <= 1400:
            return EvksPlayerRank.AMATEUR
        elif 1400 < player_state.evks_rating <= 1600:
            return EvksPlayerRank.SEMIPRO
        elif 1600 < player_state.evks_rating <= 1900:
            return EvksPlayerRank.PRO
        elif 1900 < player_state.evks_rating <= 2000:
            return EvksPlayerRank.PRO
        elif 2000 < player_state.evks_rating:
            return EvksPlayerRank.MASTER
        else:
            raise ValueError()
