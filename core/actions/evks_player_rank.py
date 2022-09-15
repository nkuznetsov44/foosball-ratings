from common.entities.player_state import PlayerState
from common.entities.enums import EvksPlayerRank as Rank
from core.actions.abstract_action import AbstractAction


class CalculateEvksPlayerRanksAction(AbstractAction[Rank]):
    def __init__(self, player_state: PlayerState) -> None:
        self.player_state = player_state

    async def handle(self) -> Rank:
        # TODO: реализовать правильную логику переходов

        if self.player_state.evks_rating <= 1000:
            return Rank.BEGINNER
        elif 1000 < self.player_state.evks_rating <= 1250:
            return Rank.NOVICE
        elif 1250 < self.player_state.evks_rating <= 1500:
            return Rank.AMATEUR
        elif 1500 < self.player_state.evks_rating <= 1750:
            return self.Rank.SEMIPRO
        elif 1750 < self.player_state.evks_rating <= 2000:
            return Rank.PRO
        elif 2000 < self.player_state.evks_rating:
            return Rank.MASTER
        else:
            raise ValueError()


# TODO: Finish implementation. Move to common.
rank_limits = {
    Rank.BEGINNER: 0,
    Rank.NOVICE: 1000,
    Rank.AMATEUR: 1250,
    Rank.SEMIPRO: 1500,
    Rank.PRO: 1750,
    Rank.MASTER: 2000,
}

ranks_order = sorted(Rank, key=rank_limits.get)


class EvksPlayerRankStateMachine:
    def __init__(self, state: Rank = Rank.BEGINNER) -> None:
        self.state = state
