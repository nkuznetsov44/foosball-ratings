import pytest
from hamcrest import assert_that, equal_to

from core.processing.calculators.evks import EvksRatingCalculator


@pytest.fixture
def calculator(ratings_state):
    return EvksRatingCalculator(ratings_state)


def test_evks_calculation_doubles(
    calculator, doubles_competition, doubles_match, doubles_match_sets
):
    result = calculator.calculate(
        competition=doubles_competition,
        match=doubles_match,
        match_sets=doubles_match_sets,
    )
    # r = 2.547396728611409795104721012
    assert_that(
        result,
        equal_to(
            {
                1: 1713,
                2: 2066,
                3: 1635,
                4: 1215,
            }
        ),
    )


def test_evks_calculation_singles(
    calculator, singles_competition, singles_match, singles_match_sets
):
    result = calculator.calculate(
        competition=singles_competition,
        match=singles_match,
        match_sets=singles_match_sets,
    )
    # r = 35.72428301468905220089739857
    assert_that(
        result,
        equal_to(
            {
                2: 2027,
                4: 1254,
            }
        ),
    )
