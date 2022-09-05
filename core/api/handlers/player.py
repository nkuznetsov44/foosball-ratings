from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from core.actions.player import CreatePlayersAction, GetPlayersAction, GetPlayerAction
from core.api.schemas.player import (
    PlayerIDSchema,
    PlayerSchema,
    CreatePlayersRequestSchema,
    GetPlayersResponseSchema,
)
from core.api.schemas.state import RatingsStateResponseSchema


class PlayerHandler(AbstractHandler):
    @request_schema(PlayerIDSchema)
    @response_schema(PlayerSchema)
    async def get(self) -> web.Response:
        get_player_request = await self.get_request_data()
        player = await GetPlayerAction(get_player_request['player_id']).run()
        return self.make_response(player)


class PlayersHandler(AbstractHandler):
    @response_schema(GetPlayersResponseSchema)
    async def get(self) -> web.Response:
        players = await GetPlayersAction().run()
        return self.make_response({"players": players})

    @request_schema(CreatePlayersRequestSchema)
    @response_schema(RatingsStateResponseSchema)
    async def post(self) -> web.Response:
        create_players_request = await self.get_request_data()
        new_state = await CreatePlayersAction(request=create_players_request).run()
        return self.make_response(new_state)
