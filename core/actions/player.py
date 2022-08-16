from core.actions.abstract_action import AbstractAction
from core.api.requests.player import CreatePlayersRequest
from core.entities.state import PlayerState


class CreatePlayersAction(AbstractAction):
    def __init__(self, request: CreatePlayersRequest) -> None:
        self.request = request

    async def run(self) -> list[PlayerState]:
        # create new players in database
        # dispatch processing.ProcessPlayer for each player
        pass
