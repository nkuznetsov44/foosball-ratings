from core.actions.abstract_action import AbstractAction
from core.api.requests.competition import CreateCompetitionRequest
from core.entities.competition import Competition


class CreateCompetitionAction(AbstractAction):
    def __init__(self, request: CreateCompetitionRequest) -> None:
        self.request = request

    async def run(self) -> Competition:
        # create new competition in database
        # create all teams, sets, matches in database
        # return Competition entity
        pass
