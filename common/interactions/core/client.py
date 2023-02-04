from common.entities.player import Player
from common.entities.competition import Competition
from common.entities.tournament import Tournament
from common.entities.match import MatchWithRelated
from common.entities.ratings_state import RatingsState
from common.entities.player_state import PlayerState
from common.entities.schemas import (
    PlayerSchema,
    CompetitionSchema,
    MatchWithRelatedSchema,
    TournamentSchema,
    RatingsStateSchema,
    PlayerStateSchema,
)
from common.interactions.core.requests.player import CreatePlayersRequest
from common.interactions.core.requests.tournament import CreateTournamentRequest
from common.interactions.core.requests.competition import CreateCompetitionRequest
from common.interactions.core.requests.schemas import (
    CreatePlayersRequestSchema,
    CreateTournamentRequestSchema,
    CreateCompetitionRequestSchema,
)
from common.interactions.base import BaseInteractionClient, InteractionClientContext


class CoreClient(BaseInteractionClient):
    def __init__(self, host: str, port: int) -> None:
        self.base_url = f"http://{host}:{port}/api/v1"

    async def get_players(self) -> list[Player]:
        resp_json = await self.get(f"{self.base_url}/players")
        return PlayerSchema(many=True).load(resp_json)

    async def get_player_competitions(self, player_id: int) -> list[Competition]:
        resp_json = await self.get(f"{self.base_url}/players/{player_id}/competitions")
        return CompetitionSchema(many=True).load(resp_json)

    async def get_player_competition_matches(
        self, player_id: int, competition_id: int
    ) -> list[MatchWithRelated]:
        resp_json = await self.get(
            f"{self.base_url}/players/{player_id}/competitions/{competition_id}/matches"
        )
        return MatchWithRelatedSchema(many=True).load(resp_json)

    async def get_tournaments(self) -> list[Tournament]:
        resp_json = await self.get(f"{self.base_url}/tournaments")
        return TournamentSchema(many=True).load(resp_json)

    async def get_tournament_competitions(self, tournament_id: int) -> list[Competition]:
        resp_json = await self.get(f"{self.base_url}/tournaments/{tournament_id}/competitions")
        return CompetitionSchema(many=True).load(resp_json)

    async def get_ratings_state(self) -> RatingsState:
        resp_json = await self.get(f"{self.base_url}/ratings_state")
        return RatingsStateSchema().load(resp_json)

    async def create_players(self, request: CreatePlayersRequest) -> list[PlayerState]:
        request_data = CreatePlayersRequestSchema().dump(request)
        resp_json = await self.post(f"{self.base_url}/players", data=request_data)
        return PlayerStateSchema(many=True).load(resp_json)

    async def create_tournament(self, request: CreateTournamentRequest) -> Tournament:
        request_data = CreateTournamentRequestSchema().dump(request)
        resp_json = await self.post(f"{self.base_url}/tournaments", data=request_data)
        return TournamentSchema().load(resp_json)

    async def create_competition(self, request: CreateCompetitionRequest) -> RatingsState:
        request_data = CreateCompetitionRequestSchema().dump(request)
        resp_json = await self.post(f"{self.base_url}/competitions", data=request_data)
        return RatingsStateSchema().load(resp_json)


class CoreClientContext(InteractionClientContext[CoreClient]):
    client_cls = CoreClient
