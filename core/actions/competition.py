from core.entities.competition import Competition
from core.actions.abstract_action import AbstractAction


class CreateCompetitionAction(AbstractAction):
    def __init__(self, competition: Competition) -> None:
        self.competition = competition
