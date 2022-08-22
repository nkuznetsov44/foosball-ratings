from common.enums import RatingType
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
)
from core.entities.competition import Competition
from core.entities.match import Match


_PlayerId = int
_RatingValue = int


class CumulativeRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.CUMULATIVE

    def calculate(
        self, match: Match, competition: Competition
    ) -> dict[_PlayerId, _RatingValue]:
        # TODO: implement cumulative rating calcuation logic
        return {player.id: 0 for player in match.players}
