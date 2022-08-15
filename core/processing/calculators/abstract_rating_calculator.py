from dataclasses import dataclass
from abc import ABC, abstractmethod
from core.entities import PlayerState, Match, Competition


@dataclass
class RatingCalculationResult:
    first_player_new_state: PlayerState
    second_player_new_state: PlayerState


class AbstractRatingCalculator(ABC):
    @abstractmethod
    async def calculate(
        self,
        first_player_state: PlayerState,
        second_player_state: PlayerState,
        match: Match,
        competition: Competition
    ) -> RatingCalculationResult:
        raise NotImplementedError()
