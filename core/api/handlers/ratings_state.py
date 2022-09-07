from aiohttp import web

from common.handlers import AbstractHandler, response_schema
from core.actions.ratings_state import GetCurrentRatingsStateAction
from core.api.schemas.ratings_state import RatingsStateResponseSchema


class RatingsStateHandler(AbstractHandler):
    @response_schema(RatingsStateResponseSchema)
    async def get(self) -> web.Response:
        ratings_state = await GetCurrentRatingsStateAction().run()
        return self.make_response(ratings_state)
