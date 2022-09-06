from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.schemas.request import PlayerIDSchema, PlayerCompetitionIDSchema
from common.schemas.entity_schemas import (
    PlayerSchema,
    CompetitionWithIDSchema,
    MatchWithIDSchema,
    PlayerWithIDSchema,
)
from core.actions.player import CreatePlayersAction, GetPlayersAction, GetPlayerAction
from core.api.schemas.player import (
    CreatePlayersRequestSchema,
)
from core.api.schemas.state import RatingsStateResponseSchema


class PlayerHandler(AbstractHandler):
    @request_schema(PlayerIDSchema)
    @response_schema(PlayerSchema)
    async def get(self) -> web.Response:
        get_player_request = await self.get_request_data()
        player = await GetPlayerAction(get_player_request["player_id"]).run()
        return self.make_response(player)


class PlayersHandler(AbstractHandler):
    @response_schema(PlayerWithIDSchema, many=True)
    async def get(self) -> web.Response:
        players = await GetPlayersAction().run()
        return self.make_response(players)

    @request_schema(CreatePlayersRequestSchema)
    @response_schema(RatingsStateResponseSchema)
    async def post(self) -> web.Response:
        create_players_request = await self.get_request_data()
        new_state = await CreatePlayersAction(request=create_players_request).run()
        return self.make_response(new_state)


class PlayerCompetitionsHandler(AbstractHandler):
    @request_schema(PlayerIDSchema)
    @response_schema(CompetitionWithIDSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        competitions = await self.core_client.get_player_competitions(**request_data)
        return self.make_response(competitions)


class PlayerCompetitionMatchesHandler(AbstractHandler):
    @request_schema(PlayerCompetitionIDSchema)
    @response_schema(MatchWithIDSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        matches = await self.core_client.get_player_competition_matches(**request_data)
        return self.make_response(matches)
