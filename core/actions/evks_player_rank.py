from typing import Sequence
from common.entities.player_state import PlayerState
from common.entities.enums import EvksPlayerRank as Rank
from common.entities.player_state import PlayerState
from core.actions.abstract_action import AbstractAction


_PlayerId = int


class CalculateEvksPlayerRanksAction(AbstractAction[list[PlayerState]]):
    def __init__(self, player_states: Sequence[PlayerState]) -> None:
        self.player_states = player_states

    async def handle(self) -> list[PlayerState]:
        for player_state in self.player_states:
            player_state.evks_rank = self._calc_rank(player_state)
        return self.player_states

    def _calc_rank(self, player_state: PlayerState) -> Rank:
        # TODO: реализовать правильную логику переходов

        if player_state.evks_rating <= 1100:
            return Rank.BEGINNER
        elif 1100 < player_state.evks_rating <= 1200:
            return Rank.NOVICE
        elif 1200 < player_state.evks_rating <= 1400:
            return Rank.AMATEUR
        elif 1400 < player_state.evks_rating <= 1600:
            return Rank.SEMIPRO
        elif 1600 < player_state.evks_rating <= 1900:
            return Rank.PRO
        elif 1900 < player_state.evks_rating:
            return Rank.MASTER
        else:
            raise ValueError()


class EvksPlayerRankStateMachine:
    _rank_limits = {
        Rank.BEGINNER: 0,
        Rank.NOVICE: 1000,
        Rank.AMATEUR: 1250,
        Rank.SEMIPRO: 1500,
        Rank.PRO: 1750,
        Rank.MASTER: 2000,
    }

    _ranks_order = [
        Rank.BEGINNER,
        Rank.NOVICE,
        Rank.AMATEUR,
        Rank.SEMIPRO,
        Rank.PRO,
        Rank.MASTER,
    ]

    def __init__(self, state: Rank = Rank.BEGINNER) -> None:
        self.state = state

    def _next_rank(self, rank: Rank) -> Rank:
        next_rank_index = self._ranks_order.index(rank) + 1
        return self._ranks_order[next_rank_index]

    def _previous_rank(self, rank: Rank) -> Rank:
        prev_rank_index = self._ranks_order.index(rank) - 1
        return self._ranks_order[prev_rank_index]

    def _upgrades_to(self, rank: Rank, evks_rating: int) -> bool:
        return self._rank_limits[rank] <= evks_rating < self._rank_limits[self._next_rank(rank)]

    def _downgrades_to(self, rank: Rank, evks_rating: int) -> bool:
        return self._rank_limits[self._previous_rank(rank)] - 100 <= evks_rating < self._rank_limits[rank] - 100

    def upgrades_to_novice(self, evks_rating: int) -> bool:
        return self._upgrades_to(Rank.NOVICE, evks_rating)

    def upgrades_to_amateur(self, evks_rating: int) -> bool:
        return self._upgrades_to(Rank.AMATEUR, evks_rating)

    def upgrades_to_semipro(self, evks_rating: int) -> bool:
        return self._upgrades_to(Rank.SEMIPRO, evks_rating)

    def upgrades_to_pro(self, evks_rating: int) -> bool:
        return self._upgrades_to(Rank.PRO, evks_rating)

    def upgrades_to_master(self, evks_rating: int) -> bool:
        return self._rank_limits[Rank.MASTER] <= evks_rating

    def downgrades_to_beginner(self, evks_rating: int) -> bool:
        return evks_rating < self._rank_limits[Rank.BEGINNER] - 100

    def downgrades_to_novice(self, evks_rating: int) -> bool:
        return self._downgrades_to(Rank.NOVICE, evks_rating)

    def downgrades_to_amateur(self, evks_rating: int) -> bool:
        return self._downgrades_to(Rank.AMATEUR, evks_rating)

    def downgrades_to_semipro(self, evks_rating: int) -> bool:
        return self._downgrades_to(Rank.SEMIPRO, evks_rating)

    def downgrades_to_pro(self, evks_rating: int) -> bool:
        return self._downgrades_to(Rank.PRO, evks_rating)
