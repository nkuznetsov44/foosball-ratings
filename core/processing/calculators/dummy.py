from dataclasses import dataclass
from typing import Sequence

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet
from common.entities.rating_calculation import BaseRatingCalculation
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
    RatingCalculationResult,
)


@dataclass(frozen=True)
class Dummy(BaseRatingCalculation):
    pass


class DummyCumulativeRatingCalculator(AbstractRatingCalculator[Dummy]):
    rating_type = RatingType.CUMULATIVE

    def calculate(
        self,
        *,
        competition: Competition,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> RatingCalculationResult[Dummy]:
        return {player.id: Dummy(value=0) for player in match.players}
