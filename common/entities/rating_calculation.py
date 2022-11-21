from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class BaseRatingCalculation:
    value: int


@dataclass(frozen=True)
class EvksCalculation(BaseRatingCalculation):
    rw: Decimal
    rl: Decimal
    t: Decimal
    d: Decimal
    k: Decimal
    r: Decimal


@dataclass(frozen=True)
class CumulativeCalculation(BaseRatingCalculation):
    pass
