from aiohttp import web
from common.handlers.abstract_handler import request_schema, response_schema
from core.api.handlers.abstract_db_handler import AbstractDbHandler
from core.api.schemas.competition import (
    CreateCompetitionRequestSchema,
    CompetitionSchema,
)
from core.actions.competition import CreateCompetitionAction


class CompetitionHandler(AbstractDbHandler):
    @request_schema(CreateCompetitionRequestSchema)
    @response_schema(CompetitionSchema)
    async def post(self) -> web.Response:
        create_competition_request = await self.get_request_data()
        competition = await self.run_action(
            CreateCompetitionAction, request=create_competition_request
        )
        self.make_response(competition)
