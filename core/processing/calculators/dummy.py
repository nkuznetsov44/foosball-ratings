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
class PlayerDummyResult(BasePlayerRatingResult):
    pass


class DummyCumulativeRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.CUMULATIVE

    def calculate(
        self,
        *,
        competition: Competition,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> RatingCalculationResult[PlayerDummyResult]:
        return {
            player.id: PlayerDummyResult(rating_value=0) for player in match.players
        }
