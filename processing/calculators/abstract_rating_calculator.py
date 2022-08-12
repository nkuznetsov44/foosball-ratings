from dataclasses import dataclass
from abc import ABC, abstractmethod
from core.entities import RatingState, PlayerState
from storage.model import Match


@dataclass
class RatingCalculationResult:
    first_player_new_state: PlayerState
    second_player_new_state: PlayerState


class AbstractRatingCalculator:
    @abstractmethod
    async def calculate(
        self,
        first_player_state: PlayerState,
        second_player_state: PlayerState,
        match: Match
    ) -> RatingCalculationResult:
        raise NotImplementedError()
