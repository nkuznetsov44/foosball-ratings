from typing import Sequence

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet
from common.entities.rating_calculation import CumulativeCalculation
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
    RatingCalculationResult,
)


class CumulativeRatingCalculator(AbstractRatingCalculator[CumulativeCalculation]):
    rating_type = RatingType.CUMULATIVE

    def calculate(
        self,
        *,
        competition: Competition,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> RatingCalculationResult[CumulativeCalculation]:
        # TODO: implement cumulative rating calcuation logic
        return {player.id: CumulativeCalculation(value=0) for player in match.players}
