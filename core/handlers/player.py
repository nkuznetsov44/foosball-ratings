from core.entities.state import PlayerState
from core.handlers.abstract_handler import AbstractHandler
from core.actions.player import CreatePlayerAction


class CreatePlayerHandler(AbstractHandler[CreatePlayerAction]):
    async def handle(self, action: CreatePlayerAction) -> PlayerState:
        # create new players
        pass
