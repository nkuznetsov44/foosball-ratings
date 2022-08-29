from aiohttp import web

from common.handlers import request_schema, response_schema
from core.actions.tournament import CreateTournamentAction
from core.api.handlers.abstract_core_handler import AbstractCoreHandler
from core.api.schemas.tournament import CreateTournamentRequestSchema, TournamentSchema


class TournamentHandler(AbstractCoreHandler):
    @request_schema(CreateTournamentRequestSchema)
    @response_schema(TournamentSchema)
    async def post(self) -> web.Response:
        create_tournament_request = await self.get_request_data()
        tournament = await self.run_action(
            CreateTournamentAction, request=create_tournament_request
        )
        return self.make_response(tournament)
