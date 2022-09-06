from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.schemas.entity_schemas import TournamentWithIDSchema
from core.actions.tournament import CreateTournamentAction
from core.api.schemas.tournament import CreateTournamentRequestSchema


class TournamentHandler(AbstractHandler):
    @request_schema(CreateTournamentRequestSchema)
    @response_schema(TournamentWithIDSchema)
    async def post(self) -> web.Response:
        create_tournament_request = await self.get_request_data()
        tournament = await CreateTournamentAction(
            request=create_tournament_request
        ).run()
        return self.make_response(tournament)
