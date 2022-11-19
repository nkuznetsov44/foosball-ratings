from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.entities.schemas import RatingsStateSchema
from common.interactions.core.requests.schemas import CreateCompetitionRequestSchema
from core.actions.competition import CreateProcessedCompetitionAction


class CompetitionHandler(AbstractHandler):
    @request_schema(CreateCompetitionRequestSchema)
    @response_schema(RatingsStateSchema)
    async def post(self) -> web.Response:
        request = await self.get_request_data()
        # TODO: catch core errors and raise common api error
        ratings_state = await CreateProcessedCompetitionAction(request=request).run()
        return self.make_response(ratings_state)
