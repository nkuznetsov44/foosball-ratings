from core.actions.abstract_action import AbstractAction, ActionContext
from core.api.requests.tournament import CreateTournamentRequest
from core.entities.tournament import Tournament


class CreateTournamentAction(AbstractAction):
    def __init__(
        self,
        *,
        context: ActionContext,
        request: CreateTournamentRequest,
    ) -> None:
        super().__init__(context)
        self._request = request

    async def run(self) -> Tournament:
        tournament = Tournament(
            name=self._request.name,
            city=self._request.city,
            start_date=self._request.start_date,
            end_date=self._request.end_date,
            url=self._request.url,
            competitions=[],
        )

        async with self._make_db_session()() as session:
            session.add(tournament)
            await session.commit()
            assert tournament.id is not None
            return tournament
