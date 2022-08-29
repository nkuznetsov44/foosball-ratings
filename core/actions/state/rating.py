from common.entities.competition import Competition
from common.entities.enums import EvksPlayerRank
from common.entities.state import PlayerState, RatingsState
from core.actions.abstract_action import AbstractAction, ActionContext

_PlayerId = int


class CreateRatingsStateAction(AbstractAction):
    def __init__(
        self,
        *,
        context: ActionContext,
        player_states: dict[_PlayerId, PlayerState],
        last_competition: Competition,
    ) -> None:
        super().__init__(context)
        self._player_states = player_states
        self._last_competition = last_competition

    def _get_evks_player_ranks(
        self, new_state: RatingsState
    ) -> dict[_PlayerId, EvksPlayerRank]:
        # TODO: реализовать логику перехода между рангами после категории
        return self.ratings_state.evks_player_ranks

    async def run(self) -> RatingsState:
        new_state = RatingsState(
            previous_state_id=self.ratings_state.id,
            last_competition=self._last_competition,
            player_states=self._player_states,
            evks_player_ranks={},
        )
        new_state.evks_player_ranks = self._get_evks_player_ranks(new_state)

        async with self.make_db_session()() as session:
            session.add(new_state)
            await session.commit()
            assert (
                new_state.id is not None
            ), "RatingsState id is null after session commit"
            self._context.ratings_state = new_state

        return new_state


class GetCurrentRatingsStateAction(AbstractAction):
    def __init__(self, context: ActionContext) -> None:
        super().__init__(context)

    async def run(self) -> RatingsState:
        return self.ratings_state
