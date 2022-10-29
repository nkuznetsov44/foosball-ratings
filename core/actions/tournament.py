from common.entities.ratings_state import RatingsState
from common.entities.tournament import Tournament
from core.actions.abstract_action import AbstractAction
from common.interactions.core.requests.tournament import (
    CreateTournamentRequest,
)


class CreateTournamentAction(AbstractAction[RatingsState]):
    def __init__(self, request: CreateTournamentRequest) -> None:
        self.request = request

    async def handle(self) -> Tournament:
        return await self.storage.tournaments.create(
            Tournament(
                id=None,
                external_id=self.request.external_id,
                name=self.request.name,
                city=self.request.city,
                url=self.request.url,
            )
        )
