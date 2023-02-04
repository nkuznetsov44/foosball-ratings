from common.entities.tournament import Tournament
from core.actions.abstract_action import AbstractAction
from common.interactions.core.requests.tournament import (
    CreateTournamentRequest,
)


class GetTournamentsAction(AbstractAction[list[Tournament]]):
    async def handle(self) -> list[Tournament]:
        return await self.storage.tournaments.lst()


class CreateTournamentAction(AbstractAction[Tournament]):
    def __init__(self, create_tournament_request: CreateTournamentRequest) -> None:
        self.request = create_tournament_request

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
