from typing import Sequence, TypeVar
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import ClassVar

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet
from common.entities.ratings_state import RatingsState


@dataclass(frozen=True)
class BasePlayerRatingResult:
    rating_value: int


T = TypeVar("T")
RatingCalculationResult = dict[int, T]


class AbstractRatingCalculator(ABC):
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
    ) -> RatingCalculationResult[BasePlayerRatingResult]:
        raise NotImplementedError()
