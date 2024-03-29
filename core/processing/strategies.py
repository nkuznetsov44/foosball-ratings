from typing import ClassVar, Type

from common.entities.enums import RatingType
from core.processing.calculators import cumulative, evks, dummy
from core.processing.calculators.abstract_rating_calculator import (
    AbstractRatingCalculator,
)


class AbstractCalculationStrategy:
    calculators: ClassVar[dict[RatingType, Type[AbstractRatingCalculator]]]


class Pre2018RatingCalculationStrategy(AbstractCalculationStrategy):
    calculators = {
        RatingType.EVKS: evks.Pre2018EvksRatingCalculator,
        RatingType.CUMULATIVE: dummy.DummyCumulativeRatingCalculator,
    }


class EvksOnlyRatingCalculationStrategy(AbstractCalculationStrategy):
    calculators = {
        RatingType.EVKS: evks.Pre2018EvksRatingCalculator,
        RatingType.CUMULATIVE: dummy.DummyCumulativeRatingCalculator,
    }


class EvksAndCumulativeRatingCalculationStrategy(AbstractCalculationStrategy):
    calculators = {
        RatingType.EVKS: evks.EvksRatingCalculator,
        RatingType.CUMULATIVE: cumulative.CumulativeRatingCalculator,
    }
