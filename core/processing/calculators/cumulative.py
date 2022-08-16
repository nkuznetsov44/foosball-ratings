from core.entities.rating import RatingType
from core.processing.calculators.abstract_rating_calculator import AbstractRatingCalculator
from core.entities.competition import Competition
from core.entities.player import Player
from core.entities.match import Match
from core.entities.state import RatingsState


class CumulativeRatingCalculator(AbstractRatingCalculator):
    rating_type = RatingType.CUMULATIVE

    async def calculate(
        self,
        ratings_state: RatingsState,
        match: Match,
        competition: Competition
    ) -> dict[Player, int]:
        # implement cumulative rating calcuation logic here
        pass
