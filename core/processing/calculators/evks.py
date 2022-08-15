from abc import abstractmethod
from enum import Enum
from typing import ClassVar, Sequence
from core.entities.rating import RatingType
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator, PlayersRatingCalculationResult
)
from core.entities.competition import Competition
from core.entities.match import Match
from core.entities.state import RatingsState


class GameType(Enum):
    QUALIFICATION = 'Qualification'
    SET_TO_5 = 'Each set to 5 points'
    SET_TO_7 = 'Each set to 7 points'


class BaseEvksRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.EVKS
    game_coefficients = ClassVar[dict[GameType, int]]

    @abstractmethod
    async def calculate(
        self,
        ratings_state: RatingsState,
        match: Match,
        competition: Competition
    ) -> Sequence[PlayersRatingCalculationResult]:
        # implement evks calculation logic here
        pass


class Pre2018EvksRatingCalculator(BaseEvksRatingCalculator):
    game_coefficients = {
        GameType.QUALIFICATION: 32,
        GameType.SET_TO_5: 24,
        GameType.SET_TO_7: 32
    }


class EvksRatingCalculator(BaseEvksRatingCalculator):
    game_coefficients = {
        GameType.QUALIFICATION: 16,
        GameType.SET_TO_5: 24,
        GameType.SET_TO_7: 32
    }
