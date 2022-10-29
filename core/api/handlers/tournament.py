from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.interactions.core.requests.schemas import (
    CreateTournamentRequestSchema,
)
from common.entities.schemas import TournamentSchema
from core.actions.tournament import CreateTournamentAction


class TournamentHandler(AbstractHandler):
    @request_schema(CreateTournamentRequestSchema)
    @response_schema(TournamentSchema)
    async def post(self) -> web.Response:
        request = await self.get_request_data()
        tournament = await CreateTournamentAction(request=request).run()
        return self.make_response(tournament)
