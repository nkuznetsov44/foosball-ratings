from common.entities.competition import Competition
from common.entities.match import Match
from common.entities.player import Player
from webapp.interactions.base import BaseInteractionClient


class CoreClient(BaseInteractionClient):
    async def get_players(self) -> list[Player]:
        pass

    async def get_player_competitions(
        self, player_id: int, competition_id: int
    ) -> list[Competition]:
        pass

    async def get_player_competition_matches(
        self, player_id: int, competition_id: int
    ) -> list[Match]:
        pass
