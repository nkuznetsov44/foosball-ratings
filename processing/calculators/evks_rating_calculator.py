from abstract_rating_calculator import AbstractRatingCalculator, RatingCalculationResult
from storage.model import Match
from core.entities import PlayerState


class EvksRatingCalculator(AbstractRatingCalculator):
    async def calculate(
        self,
        first_player_state: PlayerState,
        second_player_state: PlayerState,
        match: Match
    ) -> RatingCalculationResult:
        # implement evks calculation logic here
        pass
