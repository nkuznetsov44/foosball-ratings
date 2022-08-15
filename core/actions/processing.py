from core.actions.abstract_action import AbstractAction
from core.entities.competition import Competition
from core.entities.player import Player


class ProcessCompetitionAction(AbstractAction):
    """Обработать новую категорию"""
    def __init__(self, competition: Competition) -> None:
        self.competition = competition


class ProcessPlayersAction(AbstractAction):
    """Создать PlayerStates новых игроков"""
    def __init__(self, players: list[Player]) -> None:
        self.players = players
