import pytest_asyncio
from hamcrest import assert_that, equal_to

from core.processing.calculators.evks import EvksRatingCalculator


class TestEvksCalculation:
    def test_evks_calculation_doubles(
        self,
        calculator,
        stored_doubles_competition,
        stored_doubles_match,
        stored_doubles_match_sets,
        stored_player1,
        stored_player2,
        stored_player3,
        stored_player4,
    ):
        result = calculator.calculate(
            competition=stored_doubles_competition,
            match=stored_doubles_match,
            match_sets=stored_doubles_match_sets,
        )
        # r = 2.547396728611409795104721012
        assert_that(
            result,
            equal_to(
                {
                    stored_player1.id: 3,
                    stored_player2.id: 3,
                    stored_player3.id: -3,
                    stored_player4.id: -3,
                }
            ),
        )

    def test_evks_calculation_singles(
        self,
        calculator,
        stored_singles_competition,
        stored_singles_match,
        stored_singles_match_sets,
        stored_player2,
        stored_player4,
    ):
        result = calculator.calculate(
            competition=stored_singles_competition,
            match=stored_singles_match,
            match_sets=stored_singles_match_sets,
        )
        # r = 35.72428301468905220089739857
        assert_that(
            result,
            equal_to(
                {
                    stored_player2.id: -36,
                    stored_player4.id: 36,
                }
            ),
        )

    @pytest_asyncio.fixture
    async def calculator(self, stored_ratings_state):
        return EvksRatingCalculator(stored_ratings_state)
