from typing import ClassVar
from abc import ABC, abstractmethod
from common.enums import RatingType
from core.entities.match import Match
from core.entities.competition import Competition
from core.entities.state import RatingsState


_PlayerId = int
_RatingValue = int


class AbstractRatingCalculator(ABC):
    rating_type = ClassVar[RatingType]

    def __init__(self, ratings_state: RatingsState) -> None:
        self.ratings_state = ratings_state

    @abstractmethod
    def calculate(
        self, match: Match, competition: Competition
    ) -> dict[_PlayerId, _RatingValue]:
        raise NotImplementedError()
