from common.entities.competition import Competition
from common.entities.player import Player
from common.entities.schemas import (
    PlayerSchema,
)
from common.interactions.core.requests.player_competition_matches import (
    PlayerCompetitionMatchesResponse,
)
from common.interactions.core.requests.schemas import (
    PlayerCompetitionMatchesResponseSchema,
)
from common.interactions.base import BaseInteractionClient, InteractionClientContext


class CoreClient(BaseInteractionClient):
    base_url = "http://localhost:8080/api/v1"  # TODO: to settings

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


class CoreClientContext(InteractionClientContext[CoreClient]):
    client_cls = CoreClient
