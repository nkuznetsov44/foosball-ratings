from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.interactions.core.requests.competition import CompetitionResponse
from common.interactions.core.requests.schemas import (
    CreateTournamentRequestSchema,
    TournamentIDSchema,
    CompetitionResponseSchema,
)
from common.entities.schemas import TournamentSchema
from core.actions.tournament import GetTournamentsAction, CreateTournamentAction
from core.actions.competition import GetTournamentCompetitionsAction


class TournamentHandler(AbstractHandler):
    @response_schema(TournamentSchema, many=True)
    async def get(self) -> web.Response:
        tournaments = await GetTournamentsAction().run()
        return self.make_response(tournaments)

    @request_schema(CreateTournamentRequestSchema)
    @response_schema(TournamentSchema)
    async def post(self) -> web.Response:
        request = await self.get_request_data()
        # TODO: catch core errors and raise common api error
        tournament = await CreateTournamentAction(request=request).run()
        return self.make_response(tournament)


class TournamentCompetitionsHandler(AbstractHandler):
    @request_schema(TournamentIDSchema)
    @response_schema(CompetitionResponseSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        competitions = await GetTournamentCompetitionsAction(**request_data).run()
        response = map(CompetitionResponse.from_competition, competitions)
        return self.make_response(response)
