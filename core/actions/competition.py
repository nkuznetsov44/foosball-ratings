from decimal import Decimal
from core.actions.abstract_action import AbstractAction
from core.api.requests.competition import CreateCompetitionRequest
from core.entities.competition import Competition


class CreateCompetitionAction(AbstractAction):
    def __init__(
        self, request: CreateCompetitionRequest, evks_importance_coefficient: Decimal
    ) -> None:
        self.request = request

    async def run(self) -> Competition:
        # create new competition in database
        # create all teams, sets, matches in database
        # return Competition entity
        # Dont forget to inherit evks_importance from tournament
        # tournament = await get_tournament(id=self.request.tournament_id)
        pass
