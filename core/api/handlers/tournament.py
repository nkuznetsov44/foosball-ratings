from aiohttp import web
from common.handlers.abstract_handler import request_schema, response_schema
from core.api.handlers.abstract_db_handler import AbstractDbHandler
from core.api.schemas.tournament import (
    CreateTournamentRequestSchema,
    TournamentSchema,
)
from core.actions.tournament import CreateTournamentAction


class TournamentHandler(AbstractDbHandler):
    @request_schema(CreateTournamentRequestSchema)
    @response_schema(TournamentSchema)
    async def post(self) -> web.Response:
        create_tournament_request = await self.get_request_data()
        tournament = await self.run_action(
            CreateTournamentAction, request=create_tournament_request
        )
        return self.make_response(tournament)
