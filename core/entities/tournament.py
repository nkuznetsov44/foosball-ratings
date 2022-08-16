from decimal import Decimal
from dataclasses import dataclass
from core.entities.competition import Competition


@dataclass
class Tournament:
    id: int
    name: str
    city: str
    evks_importance_coefficient: Decimal
    competitions: list[Competition]

    def __hash__(self) -> int:
        return hash(self.id)
