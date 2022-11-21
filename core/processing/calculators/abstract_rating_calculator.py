from typing import Sequence, TypeVar, Generic
from abc import ABC, abstractmethod
from typing import ClassVar

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet
from common.entities.ratings_state import RatingsState
from common.entities.rating_calculation import BaseRatingCalculation


T = TypeVar("T", bound=BaseRatingCalculation)
RatingCalculationResult = dict[int, T]


class AbstractRatingCalculator(ABC, Generic[T]):
    rating_type = ClassVar[RatingType]

    def __init__(self, ratings_state: RatingsState) -> None:
        self.ratings_state = ratings_state

    @abstractmethod
    def calculate(
        self,
        *,
        competition: Competition,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> RatingCalculationResult[T]:
        raise NotImplementedError()
