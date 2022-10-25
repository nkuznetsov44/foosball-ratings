from common.entities.competition import Competition
from common.entities.player import Player
from common.entities.schemas import (
    PlayerSchema,
)
from common.interactions.core.requests.player_competition_matches import (
    PlayerCompetitionMatchesResponse,
)
from common.interactions.core.requests.ratings_state import RatingsStateResponse
from common.interactions.core.requests.schemas import (
    PlayerCompetitionMatchesResponseSchema,
    RatingsStateResponseSchema,
)
from common.interactions.base import BaseInteractionClient, InteractionClientContext


class CoreClient(BaseInteractionClient):
    def __init__(self, host: str, port: int) -> None:
        self.base_url = f"http://{host}:{port}/api/v1"

    async def get_players(self) -> list[Player]:
        resp_json = await self.get(f"{self.base_url}/players")
        return PlayerSchema(many=True).load(resp_json)

    async def get_player_competitions(
        self, player_id: int, competition_id: int
    ) -> list[Competition]:
        pass

    async def get_player_competition_matches(
        self, player_id: int, competition_id: int
    ) -> PlayerCompetitionMatchesResponse:
        resp_json = await self.get(
            f"{self.base_url}/players/{player_id}/competitions/{competition_id}/matches"
        )
        return PlayerCompetitionMatchesResponseSchema().load(resp_json)

    async def get_ratings_state(self) -> RatingsStateResponse:
        resp_json = await self.get(f"{self.base_url}/ratings_state")
        return RatingsStateResponseSchema().load(resp_json)


class CoreClientContext(InteractionClientContext[CoreClient]):
    client_cls = CoreClient
