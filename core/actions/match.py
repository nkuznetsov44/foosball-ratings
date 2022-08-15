from typing import Optional
from core.actions.abstract_action import AbstractAction
from core.utils import DatetimeWithTZ
from core.entities.player import Player
from core.entities.match import MatchSet


class CreateTeamAction(AbstractAction):
    def __init__(
        self,
        first_player: Player,
        second_player: Optional[Player] = None
    ) -> None:
        self.first_player = first_player
        self.second_player = second_player


class CreateMatchAction(AbstractAction):
    def __init__(
        self,
        first_team: list[Player],
        second_team: list[Player],
        sets: list[MatchSet],
        start_datetime: DatetimeWithTZ,
        end_datetime: DatetimeWithTZ,
    ) -> None:
        self.first_team = first_team
        self.second_team = second_team
        self.sets = sets
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
