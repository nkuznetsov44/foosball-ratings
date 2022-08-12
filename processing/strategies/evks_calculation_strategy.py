from strategies.abstract_calculation_strategy import AbstractCalculationStrategy
from calculators.evks_rating_calculator import EvksRatingCalculator


class AbstractCalculationStrategy(AbstractCalculationStrategy):
    calculator = EvksRatingCalculator()
