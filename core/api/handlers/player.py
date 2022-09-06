from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.schemas.request import PlayerIDSchema, PlayerCompetitionIDSchema
from common.schemas.entity_schemas import (
    PlayerSchema,
    CompetitionSchema,
    MatchSchema,
    PlayerStateSchema,
)
from core.actions.player import CreatePlayersAction, GetPlayersAction, GetPlayerAction
from core.actions.match import GetPlayerCompetitionMatchesAction
from core.actions.competition import GetPlayerCompetitionsAction
from core.api.schemas.player import (
    CreatePlayersRequestSchema,
)


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


class PlayerCompetitionsHandler(AbstractHandler):
    @request_schema(PlayerIDSchema)
    @response_schema(CompetitionSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        competitions = await GetPlayerCompetitionsAction(**request_data).run()
        return self.make_response(competitions)


class PlayerCompetitionMatchesHandler(AbstractHandler):
    @request_schema(PlayerCompetitionIDSchema)
    @response_schema(MatchSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        matches = await GetPlayerCompetitionMatchesAction(**request_data).run()
        return self.make_response(matches)
