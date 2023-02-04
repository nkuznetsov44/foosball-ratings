from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.entities.schemas import TournamentSchema
from common.interactions.core.requests.schemas import CreateTournamentRequestSchema
from core.actions.tournament import GetTournamentsAction, CreateTournamentAction


class TournamentHandler(AbstractHandler):
    @response_schema(TournamentSchema, many=True)
    async def get(self) -> web.Response:
        tournaments = await GetTournamentsAction().run()
        return self.make_response(tournaments)

    @request_schema(CreateTournamentRequestSchema, location="json")
    @response_schema(TournamentSchema)
    async def post(self) -> web.Response:
        request_data = await self.get_request_data()
        # TODO: catch core errors and raise common api error
        tournament = await CreateTournamentAction(**request_data).run()
        return self.make_response(tournament)
