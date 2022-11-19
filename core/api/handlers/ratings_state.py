from aiohttp import web

from common.handlers import AbstractHandler, response_schema
from common.entities.schemas import RatingsStateSchema
from core.actions.ratings_state import GetCurrentRatingsStateAction


class RatingsStateHandler(AbstractHandler):
    @response_schema(RatingsStateSchema)
    async def get(self) -> web.Response:
        ratings_state = await GetCurrentRatingsStateAction().run()
        return self.make_response(ratings_state)
