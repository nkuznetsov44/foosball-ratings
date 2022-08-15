from abstract_rating_calculator import AbstractRatingCalculator, RatingCalculationResult
from core.entities import PlayerState, Match, Competition


class EvksRatingCalculator(AbstractRatingCalculator):
    async def calculate(
        self,
        first_player_state: PlayerState,
        second_player_state: PlayerState,
        match: Match,
        competition: Competition
    ) -> RatingCalculationResult:
        # implement evks calculation logic here
        pass
