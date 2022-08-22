from aiohttp import web
from common.handlers import response_schema
from core.api.handlers.abstract_core_handler import AbstractCoreHandler
from core.api.schemas.state import RatingsStateResponseSchema
from core.actions.state.rating import GetCurrentRatingsStateAction


class RatingsStateHandler(AbstractCoreHandler):
    @response_schema(RatingsStateResponseSchema)
    async def get(self) -> web.Response:
        ratings_state = await self.run_action(GetCurrentRatingsStateAction)
        return self.make_response(ratings_state)
