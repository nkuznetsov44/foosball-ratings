from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.entities.schemas import PlayerSchema, PlayerStateSchema
from common.interactions.core.requests.schemas import (
    PlayerIDSchema,
    CreatePlayersRequestSchema,
)
from core.actions.player import CreatePlayersAction, GetPlayersAction, GetPlayerAction


class PlayerHandler(AbstractHandler):
    @request_schema(PlayerIDSchema)
    @response_schema(PlayerSchema)
    async def get(self) -> web.Response:
        get_player_request = await self.get_request_data()
        player = await GetPlayerAction(**get_player_request).run()
        return self.make_response(player)


class PlayersHandler(AbstractHandler):
    @response_schema(PlayerSchema, many=True)
    async def get(self) -> web.Response:
        players = await GetPlayersAction().run()
        return self.make_response(players)

    @request_schema(CreatePlayersRequestSchema)
    @response_schema(PlayerStateSchema, many=True)
    async def post(self) -> web.Response:
        create_players_request = await self.get_request_data()
        player_states = await CreatePlayersAction(request=create_players_request).run()
        return self.make_response(player_states)
