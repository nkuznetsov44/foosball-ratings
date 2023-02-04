from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.entities.schemas import CompetitionSchema, RatingsStateSchema
from common.interactions.core.requests.schemas import (
    CreateCompetitionRequestSchema,
    TournamentIDSchema,
)
from core.actions.competition import (
    GetTournamentCompetitionsAction,
    CreateProcessedCompetitionAction,
)


class CompetitionHandler(AbstractHandler):
    @request_schema(TournamentIDSchema, location="match_info")
    @response_schema(CompetitionSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        competitions = await GetTournamentCompetitionsAction(**request_data).run()
        return self.make_response(competitions)

    @request_schema(TournamentIDSchema, location="match_info")
    @request_schema(CreateCompetitionRequestSchema, location="json")
    @response_schema(RatingsStateSchema)
    async def post(self) -> web.Response:
        request_data = await self.get_request_data()
        # TODO: catch core errors and raise common api error
        ratings_state = await CreateProcessedCompetitionAction(**request_data).run()
        return self.make_response(ratings_state)
