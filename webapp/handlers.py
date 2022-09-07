from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.entities.schemas import (
    PlayerSchema,
    CompetitionSchema,
)
from common.interactions.core.requests.schemas import (
    PlayerIDSchema,
    PlayerCompetitionIDSchema,
    PlayerCompetitionMatchesResponseSchema,
)
from common.interactions.core.client import CoreClientContext
from common.interactions.referees.client import RefereesClientContext
from common.interactions.referees.schemas import RefereeSchema


class AbstractWebappHandler(AbstractHandler):
    def core_client(self):
        return CoreClientContext()

    def referees_client(self):
        return RefereesClientContext()


class PlayersHandler(AbstractWebappHandler):
    @response_schema(PlayerSchema, many=True)
    async def get(self) -> web.Response:
        async with self.core_client() as client:
            players = await client.get_players()
        return self.make_response(players)


class PlayerCompetitionsHandler(AbstractWebappHandler):
    @request_schema(PlayerIDSchema)
    @response_schema(CompetitionSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        async with self.core_client() as client:
            competitions = await client.get_player_competitions(**request_data)
        return self.make_response(competitions)


class PlayerCompetitionMatchesHandler(AbstractWebappHandler):
    @request_schema(PlayerCompetitionIDSchema)
    @response_schema(PlayerCompetitionMatchesResponseSchema)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        async with self.core_client() as client:
            response = await client.get_player_competition_matches(**request_data)
        return self.make_response(response)


class RefereesHandler(AbstractWebappHandler):
    @response_schema(RefereeSchema, many=True)
    async def get(self) -> web.Response:
        async with self.referees_client() as client:
            referees = await client.get_referees()
        return self.make_response(referees)
