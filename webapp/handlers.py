from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.schemas.request import (
    PlayerIDSchema,
    PlayerCompetitionIDSchema,
)
from common.schemas.entity_schemas import (
    PlayerSchema,
    CompetitionSchema,
    MatchSchema,
)
from webapp.interactions.core_client import CoreClient


class AbstractWebappHandler(AbstractHandler):
    @property
    def core_client(self):
        return CoreClient()


class PlayersHandler(AbstractWebappHandler):
    @response_schema(PlayerSchema, many=True)
    async def get(self) -> web.Response:
        players = await self.core_client.get_players()
        return self.make_response(players)


class PlayerCompetitionsHandler(AbstractWebappHandler):
    @request_schema(PlayerIDSchema)
    @response_schema(CompetitionSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        competitions = await self.core_client.get_player_competitions(**request_data)
        return self.make_response(competitions)


class PlayerCompetitionMatchesHandler(AbstractWebappHandler):
    @request_schema(PlayerCompetitionIDSchema)
    @response_schema(MatchSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        matches = await self.core_client.get_player_competition_matches(**request_data)
        return self.make_response(matches)
