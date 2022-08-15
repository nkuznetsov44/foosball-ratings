from core.handlers.abstract_handler import AbstractHandler


class CreateCompetitionHandler(AbstractHandler[ProcessCompetitionAction]):
    def __init__(self, current_state_with_players: RatingState) -> None:
        self.current_state = current_state_with_players

    async def handle(self, action: ProcessCompetitionAction) -> RatingState:
        pass
