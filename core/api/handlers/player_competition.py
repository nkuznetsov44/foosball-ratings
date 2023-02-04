from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.entities.schemas import CompetitionSchema, MatchWithRelatedSchema
from common.interactions.core.requests.schemas import (
    PlayerIDSchema,
    PlayerCompetitionIDSchema,
)
from core.actions.match import GetPlayerCompetitionMatchesAction
from core.actions.competition import GetPlayerCompetitionsAction


class PlayerCompetitionsHandler(AbstractHandler):
    @request_schema(PlayerIDSchema, location="match_info")
    @response_schema(CompetitionSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        competitions = await GetPlayerCompetitionsAction(**request_data).run()
        return self.make_response(competitions)


class PlayerCompetitionMatchesHandler(AbstractHandler):
    @request_schema(PlayerCompetitionIDSchema, location="match_info")
    @response_schema(MatchWithRelatedSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        matches = await GetPlayerCompetitionMatchesAction(**request_data).run()
        return self.make_response(matches)
