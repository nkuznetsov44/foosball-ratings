from typing import Sequence
from abc import ABC, abstractmethod
from typing import ClassVar

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet
from common.entities.state import RatingsState

_PlayerId = int
_RatingValue = int


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
    ) -> dict[_PlayerId, _RatingValue]:
        raise NotImplementedError()
