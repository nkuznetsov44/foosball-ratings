from common.handlers.abstract_handler import AbstractHandler
from core.api.requests.schemas import (
    CreateCompetitionRequestSchema,
    CreateCompetitionResponseSchema,
)
from core.api.requests.competition import CreateCompetitionRequest
from core.entities.competition import Competition
from core.actions.competition import CreateCompetitionAction
from common.decorators import request_schema, response_schema


class CreateCompetitionHandler(AbstractHandler):
    @request_schema(CreateCompetitionRequestSchema())
    @response_schema(CreateCompetitionResponseSchema())
    async def post(self, request: CreateCompetitionRequest) -> Competition:
        action = CreateCompetitionAction(request)
        return await self.run_action(action)
