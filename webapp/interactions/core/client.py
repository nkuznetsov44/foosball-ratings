import aiohttp

from common.entities.competition import Competition
from common.entities.match import Match
from common.entities.player import Player
from common.schemas.entity_schemas import (
    PlayerSchema,
)
from webapp.interactions.base import BaseInteractionClient


class CoreClient(BaseInteractionClient):
    base_url = "http://localhost:8080/api/v1"  # TODO: to settings

    async def get_players(self) -> list[Player]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/players") as resp:
                resp_json = await resp.json()
                return PlayerSchema(many=True).load(resp_json)

    async def get_player_competitions(
        self, player_id: int, competition_id: int
    ) -> list[Competition]:
        pass

    async def get_player_competition_matches(
        self, player_id: int, competition_id: int
    ) -> list[Match]:
        pass
