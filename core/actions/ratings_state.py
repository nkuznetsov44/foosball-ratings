from common.entities.competition import Competition
from common.entities.enums import RatingsStateStatus
from common.entities.player_state import PlayerState
from common.entities.ratings_state import RatingsState
from core.actions.abstract_action import AbstractAction
from core.actions.evks_player_rank import CalculateEvksPlayerRanksAction

_PlayerId = int


class CreateRatingsStateAction(AbstractAction[RatingsState]):
    def __init__(
        self,
        *,
        player_states: dict[_PlayerId, PlayerState],
        last_competition: Competition,
    ) -> None:
        self.player_states = player_states
        self.last_competition = last_competition

    async def handle(self) -> RatingsState:
        ratings_state = await self.storage.ratings_states.get_actual()

        player_states = await self.run_subaction(
            CalculateEvksPlayerRanksAction(self.player_states)
        )

        new_state = RatingsState(
            id=None,
            previous_state_id=ratings_state.id,
            last_competition=self.last_competition,
            player_states=player_states,
            status=RatingsStateStatus.READY_TO_PUBLISH,
        )

        return await self.storage.ratings_states.create(new_state)


class GetCurrentRatingsStateAction(AbstractAction[RatingsState]):
    async def handle(self) -> RatingsState:
        return await self.storage.ratings_states.get_actual()
