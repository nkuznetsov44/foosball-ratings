from typing import ClassVar
from calculators.abstract_rating_calculator import AbstractRatingCalculator
from calculators import evks, cumulative
from common.enums import RatingType


class AbstractCalculationStrategy:
    calculators: ClassVar[dict[RatingType, AbstractRatingCalculator]]


class Pre2018RatingCalculationStrategy(AbstractCalculationStrategy):
    calculators = {RatingType.EVKS: evks.Pre2018EvksRatingCalculator}


class EvksOnlyRatingCalculationStrategy(AbstractCalculationStrategy):
    calculators = {RatingType.EVKS: evks.Pre2018EvksRatingCalculator}


class EvksAndCumulativeRatingCalculationStrategy(AbstractCalculationStrategy):
    calculators = {
        RatingType.EVKS: evks.EvksRatingCalculator,
        RatingType.CUMULATIVE: cumulative.CumulativeRatingCalculator,
    }
