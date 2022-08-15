from typing import Sequence
from core.actions.abstract_action import AbstractAction
from core.entities.state import PlayerState
from core.entities.player import Player
from core.entities.match import Match
from core.entities.rating import RatingType


class CreatePlayerStateAction(AbstractAction):
    def __init__(
        self,
        player: Player,
        ratings: dict[RatingType, int],
        last_match: Match
    ) -> None:
        self.player = player
        self.ratings = ratings
        self.last_match = last_match


class CreateRatingsStateAction(AbstractAction):
    def __init__(self, player_states: Sequence[PlayerState]) -> None:
        self.player_states = player_states
