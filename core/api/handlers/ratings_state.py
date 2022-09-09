from aiohttp import web

from common.handlers import AbstractHandler, response_schema
from common.interactions.core.requests.ratings_state import RatingsStateResponse
from common.interactions.core.requests.schemas import RatingsStateResponseSchema
from core.actions.ratings_state import GetCurrentRatingsStateAction


class RatingsStateHandler(AbstractHandler):
    @response_schema(RatingsStateResponseSchema)
    async def get(self) -> web.Response:
        ratings_state = await GetCurrentRatingsStateAction().run()
        response = RatingsStateResponse.from_ratings_state(ratings_state)
        return self.make_response(response)
