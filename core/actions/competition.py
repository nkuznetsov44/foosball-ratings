from core.actions.abstract_action import AbstractAction, ActionContext
from core.api.requests.competition import CreateCompetitionRequest
from core.entities.competition import Competition


class CreateCompetitionAction(AbstractAction):
    def __init__(
        self,
        *,
        context: ActionContext,
        request: CreateCompetitionRequest,
    ) -> None:
        super().__init__(context)
        self._request = request

    async def run(self) -> Competition:
        pass
