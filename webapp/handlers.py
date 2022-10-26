from aiohttp import web

from common.handlers import AbstractHandler, request_schema, response_schema
from common.entities.enums import RatingType
from common.entities.schemas import (
    PlayerSchema,
    CompetitionSchema,
)
from common.interactions.core.requests.schemas import (
    PlayerIDSchema,
    PlayerCompetitionIDSchema,
    PlayerCompetitionMatchesResponseSchema,
)
from common.interactions.core.client import CoreClientContext
from common.interactions.referees.client import RefereesClientContext
from common.interactions.referees.schemas import RefereeSchema

from webapp.settings import config
from webapp.requests.ratings_state import PlayerStateResp, RatingsStateResponse
from webapp.requests.schemas import RatingsStateRequestSchema, RatingsStateResponseSchema


class AbstractWebappHandler(AbstractHandler):
    def core_client(self):
        return CoreClientContext(
            host=config['core_client']['host'],
            port=int(config['core_client']['port']),
        )

    def referees_client(self):
        return RefereesClientContext()


class PlayersHandler(AbstractWebappHandler):
    @response_schema(PlayerSchema, many=True)
    async def get(self) -> web.Response:
        async with self.core_client() as client:
            players = await client.get_players()
        return self.make_response(players)


class PlayerCompetitionsHandler(AbstractWebappHandler):
    @request_schema(PlayerIDSchema)
    @response_schema(CompetitionSchema, many=True)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        async with self.core_client() as client:
            competitions = await client.get_player_competitions(**request_data)
        return self.make_response(competitions)


class PlayerCompetitionMatchesHandler(AbstractWebappHandler):
    @request_schema(PlayerCompetitionIDSchema)
    @response_schema(PlayerCompetitionMatchesResponseSchema)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        async with self.core_client() as client:
            response = await client.get_player_competition_matches(**request_data)
        return self.make_response(response)


class RatingsStateHandler(AbstractWebappHandler):
    @request_schema(RatingsStateRequestSchema)
    @response_schema(RatingsStateResponseSchema)
    async def get(self) -> web.Response:
        request_data = await self.get_request_data()
        active_only = request_data['active_only']
        rating_type = RatingType(request_data['rating_type'])

        async with self.core_client() as client:
            core_response = await client.get_ratings_state()

        player_states = core_response.player_states
        if active_only:
            player_states = filter(lambda ps: ps.is_evks_rating_active, player_states)

        return self.make_response(
            RatingsStateResponse(
                id=core_response.id,
                rating_type=rating_type,
                player_states=[
                    PlayerStateResp(
                        player_name=f"{player_state.player.first_name} {player_state.player.last_name}",
                        evks_rank=player_state.evks_rank,
                        rating=player_state.ratings[rating_type],
                        is_evks_player_active=player_state.is_evks_rating_active,
                    )
                    for player_state in player_states
                ]
            )
        )


class RefereesHandler(AbstractWebappHandler):
    @response_schema(RefereeSchema, many=True)
    async def get(self) -> web.Response:
        async with self.referees_client() as client:
            referees = await client.get_referees()
        return self.make_response(referees)
