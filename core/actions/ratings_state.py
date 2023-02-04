from typing import Collection

from common.entities.enums import RatingsStateStatus
from common.entities.player_state import PlayerState
from common.entities.ratings_state import PlayerStateSet, RatingsState
from core.actions.abstract_action import AbstractAction
from core.actions.evks_player_rank import CalculateEvksPlayerRanksAction


class CreateRatingsStateAction(AbstractAction[RatingsState]):
    def __init__(
        self,
        *,
        player_states: Collection[PlayerState],
        last_competition_id: int,
    ) -> None:
        self.player_states = player_states
        self.last_competition_id = last_competition_id

    async def handle(self) -> RatingsState:
        current_state = await self.storage.ratings_states.get_actual()

        for player_state in self.player_states:
            player_state.evks_rank = await self.run_subaction(
                CalculateEvksPlayerRanksAction(player_state)
            )

        new_state = RatingsState(
            id=None,
            previous_state_id=current_state.id,
            last_competition_id=self.last_competition_id,
            player_states=PlayerStateSet(self.player_states),
            status=RatingsStateStatus.READY_TO_PUBLISH,
        )

        return await self.storage.ratings_states.create(new_state)


class GetCurrentRatingsStateAction(AbstractAction[RatingsState]):
    async def handle(self) -> RatingsState:
        return await self.storage.ratings_states.get_actual()
