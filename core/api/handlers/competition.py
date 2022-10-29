from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.interactions.core.requests.schemas import (
    CreateCompetitionRequestSchema,
    RatingsStateResponseSchema,
)
from common.interactions.core.requests.ratings_state import RatingsStateResponse
from core.actions.competition import CreateProcessedCompetitionAction


class CompetitionHandler(AbstractHandler):
    @request_schema(CreateCompetitionRequestSchema)
    @response_schema(RatingsStateResponseSchema)
    async def post(self) -> web.Response:
        request = await self.get_request_data()
        ratings_state = await CreateProcessedCompetitionAction(request=request).run()
        response = RatingsStateResponse.from_ratings_state(ratings_state)
        return self.make_response(response)
