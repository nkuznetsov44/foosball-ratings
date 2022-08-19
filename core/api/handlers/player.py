from aiohttp import web
from common.handlers.abstract_handler import request_schema, response_schema
from core.api.handlers.abstract_db_handler import AbstractDbHandler
from core.api.schemas.player import (
    GetPlayersResponseSchema,
    CreatePlayersRequestSchema,
    CreatePlayersResponseSchema,
)
from core.actions.player import GetPlayersAction, CreatePlayersAction


class PlayersHandler(AbstractDbHandler):
    @response_schema(GetPlayersResponseSchema)
    async def get(self) -> web.Response:
        players = await self.run_action(GetPlayersAction)
        return self.make_response({"players": players})

    @request_schema(CreatePlayersRequestSchema)
    @response_schema(CreatePlayersResponseSchema)
    async def post(self) -> web.Response:
        create_players_request = await self.get_request_data()
        player_states = await self.run_action(
            CreatePlayersAction, request=create_players_request
        )
        return self.make_response({"player_states": player_states})
