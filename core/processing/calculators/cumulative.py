from typing import Sequence

from common.entities.competition import Competition
from common.entities.enums import RatingType
from common.entities.match import Match, MatchSet
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
)

_PlayerId = int
_RatingValue = int


class CumulativeRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.CUMULATIVE

    def calculate(
        self,
        *,
        competition: Competition,
        match: Match,
        match_sets: Sequence[MatchSet],
    ) -> dict[_PlayerId, _RatingValue]:
        # TODO: implement cumulative rating calcuation logic
        return {player.id: 0 for player in match.players}
