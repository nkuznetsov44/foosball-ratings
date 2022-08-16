from core.api.handlers.abstract_handler import AbstractHandler
from core.api.requests.schemas import (
    CreatePlayersRequestSchema,
    CreatePlayersResponseSchema,
)
from core.api.requests.player import CreatePlayersRequest
from core.entities.state import PlayerState
from core.actions.player import CreatePlayersAction
from common.decorators import request_schema, response_schema


class CreateCompetitionHandler(AbstractHandler):
    @request_schema(CreatePlayersRequestSchema())
    @response_schema(CreatePlayersResponseSchema())
    async def post(self, request: CreatePlayersRequest) -> dict[str, list[PlayerState]]:
        action = CreatePlayersAction(request)
        player_states = await self.run_action(action)
        return {"players": player_states}
