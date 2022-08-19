from typing import ClassVar
from abc import ABC, abstractmethod
from common.enums import RatingType
from core.entities.player import Player
from core.entities.match import Match
from core.entities.competition import Competition
from core.entities.state import RatingsState


class AbstractRatingCalculator(ABC):
    rating_type = ClassVar[RatingType]

    @abstractmethod
    def calculate(
        self, ratings_state: RatingsState, match: Match, competition: Competition
    ) -> dict[Player, int]:
        raise NotImplementedError()
