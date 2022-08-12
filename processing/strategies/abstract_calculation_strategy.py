from abc import ABC, abstractmethod
from calculators.abstract_rating_calculator import AbstractRatingCalculator


class AbstractCalculationStrategy(ABC):
    @abstractmethod
    @property
    def calculator(self) -> AbstractRatingCalculator:
        raise NotImplementedError()
