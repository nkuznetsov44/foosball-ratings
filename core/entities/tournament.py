from dataclasses import dataclass
from core.entities.competition import Competition


@dataclass
class Tournament:
    id: int
    name: str
    city: str
    competitions: list[Competition]
