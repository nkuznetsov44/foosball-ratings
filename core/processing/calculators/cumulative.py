from itertools import chain
from common.enums import RatingType
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
)
from core.entities.competition import Competition
from core.entities.player import Player
from core.entities.match import Match


class CumulativeRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.CUMULATIVE

    def calculate(self, match: Match, competition: Competition) -> dict[Player, int]:
        # TODO: implement cumulative rating calcuation logic
        return {
            player: 0
            for player in chain(match.first_team.players, match.second_team.players)
        }
