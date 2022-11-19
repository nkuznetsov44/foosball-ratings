from common.entities.player import Player
from common.entities.player_state import PlayerState
from common.entities.schemas import (
    PlayerSchema,
    PlayerStateSchema,
    TournamentSchema,
)
from common.entities.tournament import Tournament
from common.interactions.core.requests.player_competition_matches import (
    PlayerCompetitionMatchesResponse,
)
from common.interactions.core.requests.competition import (
    CompetitionResponse,
)
from common.interactions.core.requests.ratings_state import RatingsStateResponse
from common.interactions.core.requests.player import CreatePlayersRequest
from common.interactions.core.requests.tournament import CreateTournamentRequest
from common.interactions.core.requests.competition import CreateCompetitionRequest
from common.interactions.core.requests.schemas import (
    PlayerCompetitionMatchesResponseSchema,
    RatingsStateResponseSchema,
    CreatePlayersRequestSchema,
    CreateTournamentRequestSchema,
    CreateCompetitionRequestSchema,
    CompetitionResponseSchema,
)
from common.interactions.base import BaseInteractionClient, InteractionClientContext


class CoreClient(BaseInteractionClient):
    def __init__(self, host: str, port: int) -> None:
        self.base_url = f"http://{host}:{port}/api/v1"

    async def get_players(self) -> list[Player]:
        resp_json = await self.get(f"{self.base_url}/players")
        return PlayerSchema(many=True).load(resp_json)

    async def get_player_competitions(
        self, player_id: int
    ) -> list[CompetitionResponse]:
        resp_json = await self.get(f"{self.base_url}/player/{player_id}/competitions")
        return CompetitionResponseSchema(many=True).load(resp_json)

    async def get_player_competition_matches(
        self, player_id: int, competition_id: int
    ) -> PlayerCompetitionMatchesResponse:
        resp_json = await self.get(
            f"{self.base_url}/players/{player_id}/competitions/{competition_id}/matches"
        )
        return PlayerCompetitionMatchesResponseSchema().load(resp_json)

    async def get_tournaments(self) -> list[Tournament]:
        resp_json = await self.get(f"{self.base_url}/tournaments")
        return TournamentSchema(many=True).load(resp_json)

    async def get_tournament_competitions(
        self, tournament_id: int
    ) -> list[CompetitionResponse]:
        resp_json = await self.get(
            f"{self.base_url}/tournaments/{tournament_id}/competitions"
        )
        return CompetitionResponseSchema(many=True).load(resp_json)

    async def get_ratings_state(self) -> RatingsStateResponse:
        resp_json = await self.get(f"{self.base_url}/ratings_state")
        return RatingsStateResponseSchema().load(resp_json)

    async def create_players(self, request: CreatePlayersRequest) -> list[PlayerState]:
        request_data = CreatePlayersRequestSchema().dump(request)
        resp_json = await self.post(f"{self.base_url}/players", data=request_data)
        return PlayerStateSchema(many=True).load(resp_json)

    async def create_tournament(self, request: CreateTournamentRequest) -> Tournament:
        request_data = CreateTournamentRequestSchema().dump(request)
        resp_json = await self.post(f"{self.base_url}/tournaments", data=request_data)
        return TournamentSchema().load(resp_json)

    async def create_competition(
        self, request: CreateCompetitionRequest
    ) -> RatingsStateResponse:
        request_data = CreateCompetitionRequestSchema().dump(request)
        resp_json = await self.post(f"{self.base_url}/competitions", data=request_data)
        return RatingsStateResponseSchema().load(resp_json)


class CoreClientContext(InteractionClientContext[CoreClient]):
    client_cls = CoreClient
