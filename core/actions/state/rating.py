from common.entities.competition import Competition
from common.entities.enums import EvksPlayerRank, RatingsStateStatus
from common.entities.state import PlayerState, RatingsState
from core.actions.abstract_action import AbstractAction

_PlayerId = int


class CreateRatingsStateAction(AbstractAction):
    def __init__(
        self,
        *,
        player_states: dict[_PlayerId, PlayerState],
        last_competition: Competition,
    ) -> None:
        self.player_states = player_states
        self.last_competition = last_competition

    def _get_evks_player_ranks(
        self, current_state: RatingsState, new_state: RatingsState
    ) -> dict[_PlayerId, EvksPlayerRank]:
        # TODO: реализовать логику перехода между рангами после категории
        return current_state.evks_player_ranks

    async def handle(self) -> RatingsState:
        ratings_state = await self.storage.ratings_states.get_actual()

        new_state = RatingsState(
            previous_state_id=ratings_state.id,
            last_competition=self.last_competition,
            player_states=self.player_states,
            status=RatingsStateStatus.READY_TO_PUBLISH,
            evks_player_ranks={},
        )
        new_state.evks_player_ranks = self._get_evks_player_ranks(
            current_state=ratings_state,
            new_state=new_state
        )

        return await self.storage.ratings_states.create(new_state)


class GetCurrentRatingsStateAction(AbstractAction):
    async def run(self) -> RatingsState:
        return await self.storage.ratings_states.get_actual()
