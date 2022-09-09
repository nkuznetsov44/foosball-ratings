from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.interactions.core.requests.ratings_state import RatingsStateResponse
from common.interactions.core.requests.schemas import (
    CreateTournamentRequestSchema,
    RatingsStateResponseSchema,
)
from core.actions.tournament import CreateTournamentAction


class TournamentHandler(AbstractHandler):
    @request_schema(CreateTournamentRequestSchema)
    @response_schema(RatingsStateResponseSchema)
    async def post(self) -> web.Response:
        create_tournament_request = await self.get_request_data()
        ratings_state = await CreateTournamentAction(
            request=create_tournament_request
        ).run()
        response = RatingsStateResponse.from_ratings_state(ratings_state)
        return self.make_response(response)
