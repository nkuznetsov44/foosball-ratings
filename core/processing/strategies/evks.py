from strategies.abstract_calculation_strategy import AbstractCalculationStrategy
from calculators.evks import EvksRatingCalculator


class AbstractCalculationStrategy(AbstractCalculationStrategy):
    calculator = EvksRatingCalculator()
