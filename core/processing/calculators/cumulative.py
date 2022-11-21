from dataclasses import dataclass
from typing import Sequence

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
    RatingCalculationResult,
    BasePlayerRatingResult,
)


@dataclass(frozen=True)
class PlayerCumulativeResult(BasePlayerRatingResult):
    pass


class CumulativeRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.CUMULATIVE

    def calculate(
        self,
        *,
        competition: Competition,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> RatingCalculationResult[PlayerCumulativeResult]:
        # TODO: implement cumulative rating calcuation logic
        return {
            player.id: PlayerCumulativeResult(rating_value=0)
            for player in match.players
        }
