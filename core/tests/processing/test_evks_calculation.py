from decimal import Decimal
import pytest_asyncio
from hamcrest import assert_that, equal_to

from core.processing.calculators.evks import EvksRatingCalculator, PlayerEvksResult


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
        assert_that(
            result,
            equal_to(
                {
                    stored_player1.id: PlayerEvksResult(
                        rating_value=3,
                        rw=Decimal("1945.333333333333333333333333"),
                        rl=Decimal("1498"),
                        t=Decimal("0.75"),
                        d=Decimal("1"),
                        k=48,
                        r=Decimal("2.547396728611409795104721012"),
                    ),
                    stored_player2.id: PlayerEvksResult(
                        rating_value=3,
                        rw=Decimal("1945.333333333333333333333333"),
                        rl=Decimal("1498"),
                        t=Decimal("0.75"),
                        d=Decimal("1"),
                        k=48,
                        r=Decimal("2.547396728611409795104721012"),
                    ),
                    stored_player3.id: PlayerEvksResult(
                        rating_value=-3,
                        rw=Decimal("1945.333333333333333333333333"),
                        rl=Decimal("1498"),
                        t=Decimal("0.75"),
                        d=Decimal("1"),
                        k=48,
                        r=Decimal("2.547396728611409795104721012"),
                    ),
                    stored_player4.id: PlayerEvksResult(
                        rating_value=-3,
                        rw=Decimal("1945.333333333333333333333333"),
                        rl=Decimal("1498"),
                        t=Decimal("0.75"),
                        d=Decimal("1"),
                        k=48,
                        r=Decimal("2.547396728611409795104721012"),
                    ),
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
        assert_that(
            result,
            equal_to(
                {
                    stored_player2.id: PlayerEvksResult(
                        rating_value=-36,
                        rw=Decimal("1218"),
                        rl=Decimal("2063"),
                        t=Decimal("0.75"),
                        d=Decimal("1"),
                        k=Decimal("48"),
                        r=Decimal("35.72428301468905220089739857"),
                    ),
                    stored_player4.id: PlayerEvksResult(
                        rating_value=36,
                        rw=Decimal("1218"),
                        rl=Decimal("2063"),
                        t=Decimal("0.75"),
                        d=Decimal("1"),
                        k=Decimal("48"),
                        r=Decimal("35.72428301468905220089739857"),
                    ),
                }
            ),
        )

    @pytest_asyncio.fixture
    async def calculator(self, stored_ratings_state):
        return EvksRatingCalculator(stored_ratings_state)
