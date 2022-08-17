from core.actions.abstract_action import AbstractAction, ActionContext
from core.api.requests.player import CreatePlayersRequest
from core.entities.state import PlayerState
from core.entities.player import Player
from core.actions.state import CreateInitialPlayerStateAction


class CreatePlayersAction(AbstractAction):
    def __init__(self, request: CreatePlayersRequest, context: ActionContext) -> None:
        super().__init__(context)
        self.request = request

    async def run(self) -> list[PlayerState]:
        async with self.context.db.acquire() as conn:
            for player in self.request.players:
                await conn.execute(
                    Player.table()
                    .insert()
                    .values(first_name=player.first_name, last_name=player.last_name)
                )

        # TODO: update self.request.players with ids of inserted players
        player_states: list[PlayerState] = []
        for player_req in self.request.players:
            player_states.append(
                CreateInitialPlayerStateAction(
                    context=self.context,
                    player=None,  # TODO: fixme
                    rating_values=None,  # TODO: fixme
                    matches_played=None,  # TODO: fixme
                    matches_won=None,  # TODO: fixme
                    is_evks_rating_active=None,  # TODO: fixme
                )
            )
        return player_states
