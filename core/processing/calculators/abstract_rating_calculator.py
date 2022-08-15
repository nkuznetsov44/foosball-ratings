from typing import ClassVar, Sequence
from abc import ABC, abstractmethod
from core.entities.rating import RatingType
from core.entities.player import Player
from core.entities.match import Match
from core.entities.competition import Competition
from core.entities.state import RatingsState


class PlayersRatingCalculationResult:
    player: Player
    value: int


class AbstractRatingCalculator(ABC):
    rating_type = ClassVar[RatingType]

    @abstractmethod
    async def calculate(
        self,
        ratings_state: RatingsState,
        match: Match,
        competition: Competition
    ) -> Sequence[PlayersRatingCalculationResult]:
        raise NotImplementedError()
